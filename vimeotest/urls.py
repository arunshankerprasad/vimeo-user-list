from django.conf.urls.defaults import patterns, include, url
# import the view from vimeotest
from user_list.views import list_users, search
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/?$', view=list_users, name='list_users'),
    url(r'^search/?$', view=search, name='search'),
    # url(r'^admin/', include(admin.site.urls)),
)
