from flask_restful import Resource, reqparse
from playhouse.shortcuts import model_to_dict
from api.v1.auth import auth
from api.v1.models import FollowUrl, Url
from api.v1.Resourses.User.CurrentUser import CurrentUser
from api.v1.helpers import error_message, success_message
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

        try:
            from_date = datetime.strptime(args["from_date"], "%Y-%m-%d")
            to_date = datetime.strptime(args["to_date"], "%Y-%m-%d") + timedelta(days=1) - timedelta(minutes=1)
        except ValueError:
            return error_message("Wrong date format", 400)

        if from_date > to_date:
            return error_message("The 'from_date' cant be greater than 'to_date'", 400)

        if not self.validate_group_by(group_by):
            return error_message("Wrong 'grop_by' attribute", 400)

        try:
            Url.get(Url.author_id == user_id, Url.id == link_id)
        except Url.DoesNotExist:
            return error_message("User hasn't link with provided id", 400)

        redirects = self.list_redirects(from_date, to_date, link_id)
        dates = self.list_dates(from_date, to_date, group_by)
        report = self.build_report(dates, redirects, group_by)

        return success_message("Report successfully created", 200, report)

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
        dates = [from_date]
        added_date = from_date
        while added_date < to_date:
            added_date = self.add_timedelta(added_date, group_by)
            dates.append(added_date)
        return dates

    def build_report(self, dates, redirects, group_by):

        # set report "date-points" according to group_by attribute
        report = dict.fromkeys(map(self.time_to_string, dates), 0)

        # counting redirects and group it for each point in report
        for redirect in redirects:
            for i, date in enumerate(dates):
                if i < len(dates) - 1 and date < redirect["datetime"] < (self.add_timedelta(date, group_by)):
                    str_date = self.time_to_string(date)
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
    def time_to_string(time):
        return time.strftime('%d.%m.%Y %H:%M')

    @staticmethod
    def validate_group_by(group_by):
        return group_by in ["days", "hours", "minutes"]

