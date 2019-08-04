from django.conf.urls import url
from . import views

app_name = 'visualize'
urlpatterns = [
    #url(r'^$', views.index.as_view(), name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^methodology/$', views.methodology, name='methodology'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^automation_index/$', views.automation_index, name='automation_index'),
    url(r'^skill_map/$', views.skill_map, name='skill_map'),
    url(r'^automation_ranking/$', views.automation_ranking, name='automation_ranking'),
    url(r'^sitemap.xml/$', views.sitemap, name='sitemap'),
]