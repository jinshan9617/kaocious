from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'exam.views.home', name='home'),
    url(r'^answer/(\d)+$', 'exam.views.answer'),
    url(r'^login', 'exam.views.login'),
    url(r'^questions', 'exam.views.get_questions'),
    url(r'^mkques', 'exam.views.mkquestion4test'),
    # url(r'^kaocious/', include('kaocious.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
