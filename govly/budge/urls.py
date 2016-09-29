from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sphere/$', views.spheres, name='spheres'),
    url(r'^sphere/(?P<sphere_id>[0-9]+)/ables$',
        views.sphere_quantifiables, name='sphere_quantifiables'),
    url(r'^sphere/(?P<sphere_id>[0-9]+)/ables/(?P<quantifiable_id>[0-9]+)$',
        views.sphere_quantifications, name='sphere_quantifications'),
    url(r'^sphere/(?P<sphere_id>[0-9]+)/ables/(?P<quantifiable_id>[0-9]+)/by/(?P<breakdown_method_id>[0-9]+)/treemap$',
        views.sphere_breakdowns_treemap, name='sphere_breakdowns_treemap'),
    url(r'^sphere/(?P<sphere_id>[0-9]+)/ables/(?P<quantifiable_id>[0-9]+)/by/(?P<breakdown_method_id>[0-9]+)/treemap_data$',
        views.sphere_breakdowns_treemap_data, name='sphere_breakdowns_treemap_data'),
    url(r'^sphere/(?P<sphere_id>[0-9]+)/ables/(?P<quantifiable_id>[0-9]+)/by/(?P<breakdown_method_id>[0-9]+)/column$',
        views.sphere_breakdowns_column, name='sphere_breakdowns_column'),

    url(r'^quantification/(?P<quantification_id>[0-9]+)$',
        views.quantification, name='quantification'),

    url(r'^category/(?P<category_id>[0-9]+)$',
        views.category, name='category'),

    url(r'^breakdown/(?P<breakdown_id>[0-9]+)/treemap$',
        views.breakdown_treemap, name='breakdown_treemap'),
    url(r'^breakdown/(?P<breakdown_id>[0-9]+)/treemap_data$',
        views.breakdown_treemap_data, name='breakdown_treemap_data'),
]
