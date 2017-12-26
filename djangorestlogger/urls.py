from django.conf.urls import url

from djangorestlogger import views

__author__ = 'Altuhov Kirill'

urlpatterns = [
    # url(r'^$', views.get_index_page),
    url(r'^viewer/(?P<pk>\d+)/$', views.get_body),
    url(r'^viewer/$', views.get_viewer),
    url(r'^(?P<path>.*)$', views.get_path),
]