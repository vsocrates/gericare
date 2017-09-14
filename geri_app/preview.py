from formtools.preview import FormPreview
from django.http import HttpResponseRedirect
from models import Benefactor
import uuid

from django.contrib.auth.models import User, Group

class VolunteerUploadFormPreview(FormPreview):

    def done(self, request, cleaned_data):
    	print FormPreview.form_template
        # Do something with the cleaned_data, then redirect
        # to a "success" page.
        pt_first = cleaned_data['pt_name_first']
        pt_last = cleaned_data['pt_name_last']
        pt_room = cleaned_data['pt_room']
        pt_hospital = cleaned_data['pt_hospital']
        relation = cleaned_data['family_relation']

        q1 = Benefactor.objects.filter(
            first_name=pt_first,
            last_name=pt_last,
            room_number=pt_room,
            hospital_name=pt_hospital,
            isCurrentPatient=False,
        )
        pt = None

        print "print q1 everytim", q1
        #TODO something i forgot, it has to do with the query below....
        
        if not q1:
	        #create a new user with the corresponding login information
            user = User.objects.create_user(pt_first+pt_last+str(pt_room), '', str(pt_hospital)+'geriatrics')
            user.first_name = pt_first
            user.last_name = pt_last
            new_group, created = Group.objects.get_or_create(name='benefactor')
            user.groups.add(new_group)
            user.save()

            new_uuid = uuid.uuid4()
            new_pt = Benefactor(
	            first_name=pt_first,
	            last_name=pt_last,
	            room_number=pt_room,
	            hospital_name=pt_hospital,
	            verification_code=str(new_uuid),
                user=user,
                relation=relation
	            )
            new_pt.save()
            pt = new_pt

        else:
            print "we found this pt: ", q1[0]

            #remove old user from Django auth model (username must be unique)
            username = pt_first+pt_last+str(pt_room)
            user = User.objects.get(
                username=username
            )

            "there is a user: ", user
            user.delete()
           
            #create a new one
            user = User.objects.create_user(pt_first+pt_last+str(pt_room), '', str(pt_hospital)+'geriatrics')
            user.first_name = pt_first
            user.last_name = pt_last
            new_group, created = Group.objects.get_or_create(name='benefactor')
            user.groups.add(new_group)
            user.save()

            
            pt = q1[0]

            #make the patient live again:
            pt.isCurrentPatient = True
            pt.save()

        return HttpResponseRedirect('/pt_upload_success?email='+cleaned_data['family_email']
        	+"&name="+cleaned_data['family_member_name']
        	+"&code="+pt.verification_code
        	+"&pt_first="+pt.first_name
        	+"&pt_last="+pt.last_name)