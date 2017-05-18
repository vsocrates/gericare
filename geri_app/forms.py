from django import forms

from django.conf import settings
from validators import MimetypeValidator

class MediaDocumentForm(forms.Form):
	docfile = forms.FileField(help_text="Upload a video",
							   validators=[MimetypeValidator(settings.MEDIA_MIME_TYPES)],
							   label='Upload a Video!',
							   allow_empty_file=False)

class BenefactorVerificationForm(forms.Form):
	verification = forms.CharField(label="To whom")

class VolunteerUploadForm(forms.Form):
	pt_name_first = forms.CharField(label="Patient First Name: ")
	pt_name_last = forms.CharField(label="Patient Last Name: ")
	family_member_name = forms.CharField(label= "First Family Member name: ")
	family_email = forms.EmailField()
	
	CHOICES = (('mother','mother'), ('father','father'), ('brother', 'brother') ,('sister', 'sister'),('friend', 'friend'))
	family_relation = forms.ChoiceField(choices=CHOICES)

	pt_room = forms.IntegerField()

	HOSPITAL_CHOICES = (
		('UH', 'Unvirsity Hospitals'),
		('CC','Cleveland Clinic')
	)
	pt_hospital = forms.ChoiceField(choices=HOSPITAL_CHOICES)

class PatientSearchForm(forms.Form):
	pt_fname = forms.CharField(label="Patient First Name: ")
	pt_lname = forms.CharField(label="Patient Last Name: ")
	pt_room = forms.IntegerField()
	
	HOSPITAL_CHOICES = (
		('UH', 'Unvirsity Hospitals'),
		('CC','Cleveland Clinic')
	)
	
	pt_hospital = forms.ChoiceField(choices=HOSPITAL_CHOICES)