from formtools.preview import FormPreview
from django.http import HttpResponseRedirect

class VolunteerUploadFormPreview(FormPreview):

    def done(self, request, cleaned_data):
        # Do something with the cleaned_data, then redirect
        # to a "success" page.
        
        
        return HttpResponseRedirect('/pt_upload_success?email='+cleaned_data['family_email']
        	+"&name="+cleaned_data['family_member_name']
        	+"&code="+benefactor)