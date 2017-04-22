from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from geri_app.models import MediaDocument
from geri_app.models import Benefactor
from geri_app.forms import MediaDocumentForm
from geri_app.forms import BenefactorVerificationForm
from geri_app.forms import VolunteerUploadForm
from django.contrib.auth.decorators import login_required
import re

import uuid
# Create your views here.

def index(request):
	
	template = loader.get_template('geri_app/index.html')
	context = {}
	return HttpResponse(template.render(context, request))

@login_required
def verify_benefactor(request):

    print request.build_absolute_uri(request.get_full_path())
    req_path = re.search('/verify/', request.build_absolute_uri(request.get_full_path()))
    
    if request.method == "GET" and req_path:
        template = loader.get_template('geri_app/upload.html')
        pt_code = request.GET['code']
        q = Benefactor.objects.filter(
            verification_code=pt_code
        )
        context = {}
        if q:
            context['benefactor'] = q
            context['message'] = ''
            return HttpResponse(template.render(context, request))
        else:

            return render(
                request, 
                'geri_app/index.html',
                {message:'Sorry, that is not a valid code!'}
            )
        # form2 = BenefactorVerificationForm(request.GET)
        # context = {}
        # if form2.is_valid():
        #     q1 = Benefactor.objects.filter(
        #         verification_code = request.GET.values()[0]
        #         )
            
        #     if q1:
        #         benefactor = q1.values()[0]
        #         context['benefactor'] = benefactor
        #         return HttpResponse(template.render(context, request))
        #     else:
        #         pass
        # else:
        #     form2 = BenefactorVerificationForm()

    
@login_required
def simple_upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = MediaDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = MediaDocument(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('upload'))
    else:
        form = MediaDocumentForm()  # A empty, unbound form


    # Render list page with the documents and the form
    return render(
        request,
        'geri_app/upload.html',
        {'form': form}
    )

@login_required
def view_videos(request):
    # Load documents for the list page
    documents = MediaDocument.objects.all()

    return render(
        request,
        'geri_app/view.html',
        {"documents": documents}
    )

@login_required
def pt_upload(request):
    if request.method == "GET":
        template = loader.get_template('geri_app/pt_upload.html')
        template2 = loader.get_template('geri_app/pt_code_display.html')

        form = VolunteerUploadForm(request.GET)
        context = {}
        if form.is_valid():
            pt_first = request.GET['pt_name_first'] 
            pt_last = request.GET['pt_name_last'] 
            family_name = request.GET['family_member_name'] 
            family_email = request.GET['family_email']
            relation = request.GET['family_relation']
            pt_room = request.GET['pt_room']
            pt_hospital = request.GET['pt_hospital']
            context = {'pt_name_first':pt_first,
                       'pt_name_last': pt_last,
                       'family_member_name':family_name,
                       'family_email': family_email,
                       'family_relation':relation,
                       'pt_room':pt_room,
                       'pt_hospital': pt_hospital,
                      }
            
            q1 = False
            
            if not q1:
                new_uuid = uuid.uuid4()
                new_pt = Benefactor(
                    first_name=pt_first,
                    last_name=pt_last,
                    room_number=pt_room,
                    hospital_name=pt_hospital,
                    verification_code=new_uuid
                    )
                new_pt.save()
                context['benefactor'] = new_pt

            return HttpResponse(template2.render(context, request))
        else:
            form = VolunteerUploadForm()     

    return render(
        request, 
        'geri_app/pt_upload.html',
        {'form': form}
    )

@login_required
def pt_upload_success(request):
    context = {
        "email":request.GET['email'],
        'name':request.GET['name'],
    }

    return render(
        request, 
        'geri_app/patient_upload_success.html',
        context,
    )

@login_required
def volunteer_landing(request):
    q = Benefactor.objects.filter(
            isCurrentPatient=False
        )
    context = {}
    if q:
        context['active_patients'] = q
        template = loader.get_template('geri_app/volunteer_landing.html')

    return render(
        request, 
        'geri_app/volunteer_landing.html',
        context
    )