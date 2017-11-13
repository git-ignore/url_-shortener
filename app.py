from api.v1.Resourses.User.Registration import Registration
from api.v1.Resourses.User.CurrentUser import CurrentUser
from api.v1.Resourses.URLs.SingleUrl import SingleUrl
from api.v1.Resourses.Reports.Referers import ReferrersReport
from api.v1.Resourses.Reports.Redirects import RedirectsReport
from api.v1.Resourses.URLs.Redirect import Redirect
from api.v1.Resourses.URLs.Urls import Urls
from flask_restful import Api
from flask import Flask

app = Flask(__name__)
api = Api(app)

# User resource
api.add_resource(Registration, '/api/v1/users', endpoint='Registration')
api.add_resource(CurrentUser, '/api/v1/users/me', endpoint='CurrentUser')

# Urls resource
api.add_resource(Urls, '/api/v1/users/me/shorten_urls', endpoint='Urls')
api.add_resource(SingleUrl, '/api/v1/users/me/shorten_urls/<int:id>', endpoint='SingleUrl')
api.add_resource(Redirect, '/api/v1/shorten_urls/<string:hash>', endpoint='Redirect')

# Reports resource
api.add_resource(ReferrersReport, '/api/v1/users/me/shorten_urls/<int:link_id>/referrers', endpoint='ReferrersReport')
api.add_resource(RedirectsReport,
                 '/api/v1/users/me/shorten_urls/<int:link_id>/<string:group_by>',
                 endpoint='RedirectsReport'
                 )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
