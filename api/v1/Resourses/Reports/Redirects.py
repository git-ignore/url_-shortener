from flask_restful import Resource, reqparse
from playhouse.shortcuts import model_to_dict
from api.v1.auth import auth
from api.v1.models import FollowUrl
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
        from_date = datetime.strptime(args["from_date"], "%Y-%m-%d")
        to_date = datetime.strptime(args["to_date"], "%Y-%m-%d") + timedelta(days=1) - timedelta(minutes=1)
        raw_redirects = FollowUrl.select().where(
            (FollowUrl.datetime >= from_date) &
            (FollowUrl.datetime <= to_date) &
            (FollowUrl.link_id == link_id)
        ).execute()

        redirects = []
        for raw_redirect in raw_redirects:
            redirects.append(model_to_dict(raw_redirect))

        dates = self.get_dates_array(from_date, to_date, group_by)
        report = self.group_redirects(dates, redirects, group_by)

        return report

    def get_dates_array(self, from_date, to_date, group_by):
        dates = [from_date]
        added_date = from_date
        while added_date < to_date:
            added_date = self.add_timedelta(added_date, group_by)
            dates.append(added_date)
        return dates

    def group_redirects(self, dates, redirects, group_by):

        # set report points according to group_by attribute
        report = dict.fromkeys(map(self.time_to_string, dates), 0)

        # counting redirects and group for each point in report
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

