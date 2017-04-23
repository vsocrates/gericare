from django.conf.urls import url
from forms import VolunteerUploadForm
from forms import PatientSearchForm
from preview import VolunteerUploadFormPreview
from preview import PatientSearchFormPreview
from django import forms

from . import views

urlpatterns = [
	url(r'^pt_upload/', VolunteerUploadFormPreview(VolunteerUploadForm), name = "patient_upload"),
	url(r'^patient_search/', PatientSearchFormPreview(PatientSearchForm), name = "pt_search"),
	url(r'^pt_find/', views.pt_find, name='pt_find'),
	url(r'^pt_upload_success/', views.pt_upload_success, name = "patient_upload_success"),
	url(r'^verify/', views.verify_benefactor, name="verify_benefactor"),
	url(r'^view/', views.view_videos, name="view"),
    url(r'^upload/', views.simple_upload, name='upload'),
    url(r'^volunteer/', views.volunteer_landing, name="volunteer"),
    url(r'^$', views.index, name='index'),

]