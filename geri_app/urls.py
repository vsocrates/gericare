from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^pt_upload/', views.pt_upload, name = "patient_upload"),
	url(r'^verify/', views.verify_benefactor, name="verify_benefactor"),
	url(r'^view/', views.view_videos, name="view"),
    url(r'^upload/', views.simple_upload, name='upload'),
    url(r'^$', views.index, name='index'),

]