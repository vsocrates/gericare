from formtools.preview import FormPreview
from django.http import HttpResponseRedirect
from models import Benefactor
import uuid

class VolunteerUploadFormPreview(FormPreview):

    def done(self, request, cleaned_data):
    	print FormPreview.form_template
        # Do something with the cleaned_data, then redirect
        # to a "success" page.
        pt_first = cleaned_data['pt_name_first']
        pt_last = cleaned_data['pt_name_last']
        pt_room = cleaned_data['pt_room']
        pt_hospital = cleaned_data['pt_hospital']


        q1 = Benefactor.objects.filter(
            first_name=pt_first,
            last_name=pt_last,
            room_number=pt_room,
            hospital_name=pt_hospital
        )

        pt = None

        #TODO something i forgot, it has to do with the query below....
        
        if not q1:
	        new_uuid = uuid.uuid4()
	        new_pt = Benefactor(
	            first_name=pt_first,
	            last_name=pt_last,
	            room_number=pt_room,
	            hospital_name=pt_hospital,
	            verification_code=str(new_uuid)
	            )
	        new_pt.save()
	        pt = new_pt
        else:
        	pt = q1[0]

        return HttpResponseRedirect('/pt_upload_success?email='+cleaned_data['family_email']
        	+"&name="+cleaned_data['family_member_name']
        	+"&code="+pt.verification_code
        	+"&pt_first="+pt.first_name
        	+"&pt_last="+pt.last_name)




