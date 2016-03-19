from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from zombieapp import views

urlpatterns = patterns('',
<<<<<<< HEAD
    # Examples:
    # url(r'^$', 'zomb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',views.index, name='index'),
=======
>>>>>>> 716d89f7baad635312d03ee2c2910872989e8d2a
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('zombieapp.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
