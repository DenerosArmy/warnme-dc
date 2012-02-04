from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from main.views import home, food, food_profile
from main.views import user_profile, rate, login_user, logout_user, register_user
from menu.views import gendb

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        ('^$', home),                       # home page/menu
        ('^home/$', home),                   # home page/menu
        ('^food/$', food),                   # list all the food
        ('^food/id/(\d{6})/$', food_profile),   # specific food page
        ('^profile/$', user_profile),   # specific user profile
        ('^rate/(\d+)/(\d)/$', rate),                   # rate a given food
        ('^run/gendb/$', gendb),   # specific user profile
        ('^login/$', login_user),
        ('^logout/$', logout_user),
        ('^register/$', register_user),
    # Examples:
    # url(r'^$', 'warnme_dc.views.home', name='home'),
    # url(r'^warnme_dc/', include('warnme_dc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += staticfiles_urlpatterns()
