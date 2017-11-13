from flask_restful import Resource
from playhouse.shortcuts import model_to_dict
from api.v1.auth import auth
from api.v1.models import Url, FollowUrl


class ReferrersReport(Resource):

    @auth.login_required
    def get(self, link_id):
        redirects = FollowUrl.select().where(FollowUrl.link_id == link_id).execute()
        referrer_stat = {}

        # Counting of redirects from each referrer
        for row in redirects:
            referrer = model_to_dict(row)["referrer"]
            if referrer != "None":
                if referrer not in referrer_stat:
                    referrer_stat[referrer] = 1
                else:
                    referrer_stat[referrer] += 1

        # Sort and make an easy-readable view of statistics
        sorted_keys = sorted(referrer_stat.items(), key=lambda x: x[1], reverse=True)
        referrer_stat = []
        for v in sorted_keys:
            referrer_stat.append({
                "referrer": v[0],
                "count_of_redirects": v[1]
            })

        # return first 20 items (Top-20)
        return referrer_stat[:20]
