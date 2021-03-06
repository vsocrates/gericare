from django.conf.urls import url

from forms import PatientSearchForm
from forms import VolunteerUploadForm
from preview import VolunteerUploadFormPreview

from django import forms

from . import views

urlpatterns = [
	url(r'^patient_search/', views.patient_search, name = "pt_search"),
	url(r'^pt_upload/', views.pt_upload, name = "patient_upload"),
	url(r'^pt_upload2/', VolunteerUploadFormPreview(VolunteerUploadForm), name = "patient_upload2"),
	url(r'^patient_video/', views.pt_video, name="patient_video"),
	url(r'^pt_find/', views.pt_find, name='pt_find'),
	url(r'^pt_upload_success/', views.pt_upload_success, name = "patient_upload_success"),
	url(r'^verify/', views.verify_benefactor, name="verify_benefactor"),
	url(r'^view/', views.view_videos, name="view"),
    url(r'^upload/', views.simple_upload, name='video_upload'),
    url(r'^webcam_upload/', views.webcam_upload, name = 'webcam_upload'),
    url(r'^volunteer/', views.volunteer_landing, name="volunteer"),
    url(r'^seenvideo/', views.seen, name="seen"),
    url(r'^removept/', views.removept, name="removept"),
    url(r'^aboutus/', views.about_us, name="aboutus"),
    url(r'^$', views.index, name='index'),

]
