from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'home.html'}),
                       
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
        {'url': '/static/images/default/favicon.ico'}),
                                              
    url(r'^debug/form/$', 'votuition.views.form_sample'),                           
    url(r'^debug/form_json/$', 'votuition.views.form_json'),                           
    url(r'^debug/form_response/$', 'votuition.views.form_response'),              
    
    url(r'^api/(.+)/vote', 'api.handlers.vote'),             
)
