from django.conf.urls.defaults import patterns, include, url
# import the view from vimeotest
from user_list.views import list_users, get_users
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/?$', view=list_users, name='list_users'),
    url(r'^get/?$', view=get_users, name='get_users'),
    url(r'^admin/', include(admin.site.urls)),
)
