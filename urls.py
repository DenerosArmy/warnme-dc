from django.conf.urls.defaults import patterns, include, url
from main.views import home, food, food_profile, user_profile

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
        ('^$', home),                       # home page/menu
        ('^home/$', home),                   # home page/menu
        ('^food/$', food),                   # list all the food
        ('^food/id/(\d{6})/$', food_profile),   # specific food page
        ('^user/id/(\d{6})/$', user_profile),   # specific user profile
    # Examples:
    # url(r'^$', 'warnme_dc.views.home', name='home'),
    # url(r'^warnme_dc/', include('warnme_dc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
