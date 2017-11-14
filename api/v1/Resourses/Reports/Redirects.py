from flask_restful import Resource, reqparse
from playhouse.shortcuts import model_to_dict
from api.v1.auth import auth
from api.v1.models import FollowUrl, Url
from api.v1.Resourses.User.CurrentUser import CurrentUser
from api.v1.helpers import api_response_error, api_response_success, time_to_string
from datetime import datetime, timedelta


class RedirectsReport(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('from_date', type=str, required=True, help='No start date provided', location='args')
        self.reqparse.add_argument('to_date', type=str, required=True, help='No end date provided', location='args')
        super(RedirectsReport, self).__init__()

    @auth.login_required
    def get(self, link_id, group_by):
        args = self.reqparse.parse_args()
        user_id = CurrentUser.get_user_by_login(auth.username())["id"]

        # params validation
        try:
            from_date = datetime.strptime(args["from_date"], "%Y-%m-%d")
            to_date = datetime.strptime(args["to_date"], "%Y-%m-%d")
            if to_date == from_date:
                to_date += + timedelta(hours=23)
            else:
                to_date += + timedelta(days=1)
        except ValueError:
            return api_response_error("Wrong date format", 400)

        if from_date > (to_date - timedelta(hours=23)):
            return api_response_error("The 'from_date' cant be greater than 'to_date'", 400)

        if to_date > (datetime.now() + timedelta(hours=23)):
            return api_response_error("The 'to_date' cant be greater than today's datetime", 400)

        if not self.validate_group_by(group_by):
            return api_response_error("Wrong 'grop_by' attribute", 400)

        try:
            url_created = Url.get(Url.author_id == user_id, Url.id == link_id).created
        except Url.DoesNotExist:
            return api_response_error("User hasn't link with provided id", 404)

        if (from_date + timedelta(hours=23)) < url_created:
            return api_response_error("'from_date' attribute cant be earlier than link was created", 400)

        # building report
        redirects = self.list_redirects(from_date, to_date, link_id)
        dates = self.list_dates(from_date, to_date, group_by)
        report = self.build_report(dates, redirects, group_by)

        return api_response_success(report, 200)

    @staticmethod
    def list_redirects(from_date, to_date, link_id):
        raw_redirects = FollowUrl.select().where(
            (FollowUrl.datetime >= from_date) &
            (FollowUrl.datetime <= to_date) &
            (FollowUrl.link_id == link_id)
        ).execute()

        redirects = []
        for raw_redirect in raw_redirects:
            redirects.append(model_to_dict(raw_redirect))
        return redirects   
            
    def list_dates(self, from_date, to_date, group_by):
        dates = []
        added_date = from_date
        # while added_date < to_date:
        #     added_date = self.add_timedelta(added_date, group_by)
        #     dates.append(added_date)
        while True:
            dates.append(added_date)
            added_date = self.add_timedelta(added_date, group_by)
            if added_date >= to_date:
                break
        return dates

    def build_report(self, dates, redirects, group_by):

        # set report "date-points" according to group_by attribute
        report = dict.fromkeys(map(time_to_string, dates), 0)

        # counting redirects and group it for each point in report
        for redirect in redirects:
            for i, date in enumerate(dates):
                if i < len(dates) and date < redirect["datetime"] < (self.add_timedelta(date, group_by)):
                    str_date = time_to_string(date)
                    report[str_date] += 1

        return report

    @staticmethod
    def add_timedelta(date, group_by):
        if group_by == "days":
            date += timedelta(days=1)
        elif group_by == "hours":
            date += timedelta(hours=1)
        elif group_by == "minutes":
            date += timedelta(minutes=1)
        else:
            return False
        return date

    @staticmethod
    def validate_group_by(group_by):
        return group_by in ["days", "hours", "minutes"]