from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from bcapp.views import main, user, trade, database, post_comment, display_meta, search, regform, a, login, me, logout, register, addcomment, edittext, addmonster, addtradepost, edittradepost, editmonster, deletetradepost, deletemonster, addlikeu, addliked, addlikep, screenshots, deletescreenshot, addscreenshot, removelikep, messages_mine, messages_other, accepttrade, addoffer, moremonsters, removelikeu, morecomments

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Mydjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^user/(\d{1,10})/$', user),
    url(r'^main/(\d{1,10})/$', main),
    url(r'^trade/(\d{1,10})/$', trade),
    url(r'^database/(\d{1,10})/$', database),
    url(r'^post/(\d{1,10})/$', post_comment),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^meta/$', display_meta),
    url(r'^search/$', search),
    url(r'^auth/$', regform),
    url(r'^a/$', a),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^user/$', me),
    url(r'^register/$', register),
    url(r'^addcomment/(\d{1,10})/$', addcomment),
    url(r'^edittext/$', edittext),
    url(r'^addmonster/$', addmonster),
    url(r'^addtradepost/$', addtradepost),
    url(r'^edittradepost/$', edittradepost),
    url(r'^deletetradepost/$', deletetradepost),
    url(r'^editmonster/$', editmonster),
    url(r'^deletemonster/$', deletemonster),
    url(r'^deletescreenshot/$', deletescreenshot),
    url(r'^addscreenshot/$', addscreenshot),
    url(r'^addlikeu/$', addlikeu),
    url(r'^addliked/$', addliked),
    url(r'^addlikep/$', addlikep),
    url(r'^addoffer/$', addoffer),
    url(r'^accepttrade/$', accepttrade),
    url(r'^removelikep/$', removelikep),
    url(r'^removelikeu/$', removelikeu),
    url(r'^screenshots/(\d{1,10})/$', screenshots),
    url(r'^messages/(\d{1,10})/mine/$', messages_mine),
    url(r'^messages/(\d{1,10})/other/$', messages_other),
    url(r'^moremonsters/$', moremonsters),
    url(r'^morecomments/$', morecomments),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))


