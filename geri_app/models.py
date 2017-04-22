from __future__ import unicode_literals

from django.db import models
import uuid 

class Benefactor(models.Model):
	verification_code = models.CharField(default=uuid.uuid4, editable=False, max_length=30)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	room_number = models.IntegerField()
	isCurrentPatient = models.BooleanField(default=True)
	patientCheckedOutDate = models.DateField(blank=True, null=True)

	HOSPITAL_CHOICES = (
		('UH', 'Unvirsity Hospitals'),
		('CC','Cleveland Clinic')
	)
	hospital_name = models.CharField(max_length=2, choices=HOSPITAL_CHOICES, default='UH')
	
class MediaDocument(models.Model):
	docfile = models.FileField(upload_to="documents/%Y/%m/%d")
	benefactor_id = models.ForeignKey('Benefactor',on_delete=models.CASCADE)

