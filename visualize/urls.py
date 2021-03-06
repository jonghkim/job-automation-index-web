from django.conf.urls import url
from . import views

app_name = 'visualize'
urlpatterns = [
    #url(r'^$', views.index.as_view(), name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^automation_index/$', views.automation_index, name='automation_index'),
    url(r'^automation_ranking/$', views.automation_ranking, name='automation_ranking'),
    url(r'^job_automation/$', views.job_automation, name='job_automation'),
    url(r'^skill_dna/$', views.skill_dna, name='skill_dna'),        
    url(r'^skill_dna_view/$', views.skill_dna_view, name='skill_dna_view'),        
    url(r'^skill_dna_view_mobile/$', views.skill_dna_view_mobile, name='skill_dna_view_mobile'),        
    url(r'^automation_map/$', views.automation_map, name='automation_map'),                
    url(r'^city_automation/$', views.city_automation, name='city_automation'),            
    url(r'^sitemap.xml/$', views.sitemap, name='sitemap'),
]