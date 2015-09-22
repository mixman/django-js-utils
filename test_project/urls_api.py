from django.conf.urls import patterns, include, url

import test_project.views as views

urlpatterns = [
    url(r'^computer/(?P<id>[0-9]+)/license/(?P<field_pk>[0-9]+)$', views.index, name="computer-license-detail"),
]
