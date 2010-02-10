from django.conf.urls.defaults import *

urlpatterns = patterns('ebserv.apps.restful_dictionary.views',
    (r'^search/$', 'search'), #TODO search for each book? or just keep in this RPC gateway URL...
    #(r'^(.+)/entry/(.+)/$', 'entry'),
    (r'^books/$', 'books'),
    (r'^book/(.+)/subbook/(.+)/entry/(.+)/$', 'entry'),
    (r'^book/(.+)/$', 'book'), #subbooks
    #(r'^book/(.+)/subbook/(.+)/$', 'subbook'),
    
)
