from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
# import the view from vimeotest
from user_list.views import list_users, search, upload
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.conf import settings

urlpatterns = patterns('',
    url(r'^/?$', view=list_users, name='list_users'),
    url(r'^search/?$', view=search, name='search'),
    url(r'^upload/?$', view=upload, name='upload'),
    # url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
