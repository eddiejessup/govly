from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<category_id>[0-9]+)/$', views.children, name='children'),
]
