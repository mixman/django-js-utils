from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

import test_project.views as views

urlpatterns = [
    url(r'^index$', views.index, name="index"),
    url(r'^api/', include('test_project.urls_api')),
    url(r'^model/(?P<model>\w+)/(?P<id>\d+)$', views.index, name='model-view'),
]
