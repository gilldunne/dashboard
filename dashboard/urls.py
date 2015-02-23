from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from dashboardIBM.views import views

#
# Some of these endpoints have been established to solely view the data
# and ensure the data is being pulled correctly from the DB
#

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # static home page - shows the links to the various endpoints
    url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),

    # TODO - Amend this endpoint to receive live data from the DB
    # Testing a horizontal bar chart
    url(r'^api/test', TemplateView.as_view(template_name='buildjob.html'), name="test"),

    # TODO - Sort the endpoint to suit the data
    # Show a list of True or False based on the active or inactive server
    # this will have to change when the new data is clarifies
    # url /api/active-jobs/ to view the active/inactive jobs
    url(r'^api/active-jobs', views.get_active_inactive_build_jobs),

    # TODO - This displays the buildjob names and the number of each per domain
    # this will have to change when the new data is added
    # url /api/buildjob/ to view the all buildjob per team
    url(r'^api/buildjob', views.get_all_buildjob),

    # TODO - This endpoint may not be necessary.
    # url /api/users/ to view the all user per domain
    url(r'^api/users', views.get_users),

)
