from django.conf.urls import patterns, include, url
from django.http import HttpResponse, FileResponse
 
urlpatterns = patterns('app_purly.views',
    url(r'^;', 'triage'),

    url(r'^$', 'redirect_to_home'),
    # url(r'^$', 'shorten'),

    url(r'\w{1,18}-$', 'is_short_taken'),

                       # url(r'^shorten/?(?P<short_code_requested>[^/]+)/?(?P<long_url_specified>(https?|mailto|tel|data):.*)$', 'shorten', name='shorten'),
    url(r'^shorten/?(?P<long_url_specified>.*)$', 'shorten', name='shorten'),
    url(r'^qr(?P<pixels_square>[0-9]+)(?P<format_extension>[a-z]+)/?(?P<data_to_encode>.*)$', 'qr_code'),

                       # redirect short to long, for any short base with no path suffix, e.g. go.spe.org/atce
#    url(r'^(?P<short_code>\w{1,18})$', 'redirect', name='redir'),

    #    url(r'^send_link_info/(?P<recipients>[^/]+)/(?P<short_base>.+/)(?P<short_code>\w{4,30})$', 'get_link_info'),
    # url(r'^(?P<short_base_path>.+/)(?P<short_code>\w{1,18})(?P<recipients>\+)$', 'get_link_info'),
    # url(r'\+$', 'get_link_info'),
    # url(r'^(?P<short_base_path>.+/)(?P<short_code>\w{1,18})\+$', 'get_link_info'),
    # url(r'^(.+/)?(?P<short_code>\w{1,18})\+$', 'test'),
    # url(r'^(?P<short_base_path>.+/)(?P<short_code>\w{1,18})(?P<recipients>[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+|\+)$', 'get_link_info'),
    #    url(r'^send_link_info/(?P<recipients>[^/]+)/(?P<short_url>(https?://.+/\w{4,30})$)', 'send_link_info'),

    # url(r'^send_link_info/(?P<recipients>[^/]+)/(?P<short_code>\w{1,18})$', 'get_link_info'),
    url(r'^(send_link_info/)?(?P<short_code>\w{1,18})/(?P<recipients>[^/]*)$', 'get_link_info'),
    # url(r'^(?P<short_code>\w{1,18})/(?P<recipients>[^/]+)$', 'get_link_info'),

                       #    url(r'^link/(?P<short_base>[^/]+/)(?P<short_url>\w{4,30})$', 'show_link_info'),
#    url(r'^(?P<short_code>\w{4,30})\+$', 'preview', name='preview'),
#    url(r'^(?P<short_code>\w{4,30}):$', 'edit', name='edit'),

    # redirect short to long, for any short base with a path suffix, e.g. www.spe.org/go/atce
    # url(r'^(?P<short_base_path>.+/)(?P<short_code>\w{1,18})$', 'redirect', name='redir'),

#    url(r'favicon\.ico(\?.*)?$', HttpResponse('')),
#    url(r'favicon\.ico(\?.*)?$', str(FileResponse(open('favicon.ico', 'rb')))),
    url(r'.', 'triage'),

    )
