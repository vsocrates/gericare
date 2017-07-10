from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.timezone import now

import uuid 
import os 

class Benefactor(models.Model):
	verification_code = models.CharField(default=uuid.uuid4, editable=False, max_length=30)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	room_number = models.IntegerField()
	isCurrentPatient = models.BooleanField(default=True)
	patientCheckedOutDate = models.DateField(blank=True, null=True)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

	HOSPITAL_CHOICES = (
		('UH', 'Unvirsity Hospitals'),
		('CC','Cleveland Clinic')
	)
	hospital_name = models.CharField(max_length=2, choices=HOSPITAL_CHOICES, default='UH')

	RELATION = (

		("mother", "mother"),
		("father", "father"),
		("brother", "brother"),
		("sister", "sister"),
		("friend", "friend")
	)
	relation = models.CharField(max_length=30, choices=RELATION, default="friend")

class MediaDocument(models.Model):
	docfile = models.FileField(upload_to="documents/%Y/%m/%d")
	benefactor = models.ForeignKey('Benefactor',on_delete=models.CASCADE, null=True)
	uploaded_at = models.DateTimeField(default=now, editable=False)
	hasBeenViewed = models.BooleanField(default=False)

	def filename(self):
		return os.path.basename(self.docfile.name)

