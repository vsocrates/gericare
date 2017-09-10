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
import re

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from forms import VolunteerUploadForm
from preview import VolunteerUploadFormPreview
from decorators import group_required

from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.

def index(request):
	
	template = loader.get_template('geri_app/index.html')
	context = {}
	return HttpResponse(template.render(context, request))

def verify_benefactor(request):
    request.session['form-submitted'] = True
    req_path = re.search('/verify/', request.build_absolute_uri(request.get_full_path()))
    form = MediaDocumentForm(request.POST, request.FILES)

    if request.method == "GET" and req_path:
        template = loader.get_template('geri_app/patient_video.html')
        pt_code = request.GET['code']
        q = Benefactor.objects.filter(
            verification_code=pt_code
        )
        context = {}
        if q:
            context['benefactor'] = q[0]
            context['message'] = ''
            context['form'] = form
            context['verification_code'] = pt_code
            return HttpResponse(template.render(context, request))
        else:

            return render(
                request, 
                'geri_app/index.html',
                {'message':'Sorry, that is not a valid code!'}
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


def pt_video(request):
    if not request.session.get('form-submitted', False):
        request.session['form-submitted'] = False
        return HttpResponseRedirect('/pt_find')

    else:
        request.session['form-submitted'] = False
        return render(
            request,
            'geri_app/patient_video.html',
            {'verification_code':request.GET['code']
            }
        )

def simple_upload(request):
    # Handle file upload

    #print "GET", request.POST
    if request.method == 'POST':
        form = MediaDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            code = request.POST['code']
            cur_benefactor = Benefactor.objects.get(verification_code=code)
            newdoc = MediaDocument(docfile=request.FILES['docfile'], benefactor=cur_benefactor)
            newdoc.save()

            #print "new document saved!"
            # Redirect to the document list after POST
            return HttpResponseRedirect('/')
    else:
        form = MediaDocumentForm()  # A empty, unbound form
        try:
            code = request.GET['code']
            print 'code',code
            cur_benefactor = Benefactor.objects.get(verification_code=code)
        except ObjectDoesNotExist:
            print("That user doesn't exist.")

        return render(
            request,
            'geri_app/upload.html',
            {'form': form,
             'benefactor':cur_benefactor,
             'message':''
            }
        )

def webcam_upload(request):
    print "help", request
    if request.method == 'POST':
        print "post request!", request.POST
        code = request.POST['code']
        cur_benefactor = Benefactor.objects.get(verification_code=code)
        newdoc = MediaDocument(docfile=request.POST["file"], benefactor=cur_benefactor)
        newdoc.save()

        print "new document saved!"
            # Redirect to the document list after POST
        return HttpResponseRedirect('/')
    
    else:
        form = MediaDocumentForm()  # A empty, unbound form
        try:
            code = request.GET['code']
            #print 'code',code
            cur_benefactor = Benefactor.objects.get(verification_code=code)
        except ObjectDoesNotExist:
            print("That user doesn't exist.")

        return render(
            request,
            'geri_app/webcam_upload.html',
            {'form': form,
             'benefactor':cur_benefactor,
             'message':''
            }
        )

@group_required('benefactor')
def view_videos(request):
    # Load documents for the list page
    current_user = request.user
    print 'current user ', current_user
    documents = []
    try:
        cur_benefactor = Benefactor.objects.get(user = current_user)
        documents = MediaDocument.objects.filter(
        benefactor_id=cur_benefactor
        )
    except ObjectDoesNotExist:
        print("That user doesn't exist.")

    return render(
        request,
        'geri_app/view.html',
        {"documents": documents,
         "media_url": settings.MEDIA_URL}
    )

@group_required('volunteer')
def pt_upload(request):
    print "did the volunteer upload preview"
    return HttpResponseRedirect('/pt_upload2')

#     if request.method == "GET":
#         template = loader.get_template('geri_app/pt_upload.html')
#         template2 = loader.get_template('geri_app/pt_code_display.html')

#         form = VolunteerUploadForm(request.GET)
#         context = {}
#         if form.is_valid():
#             pt_first = request.GET['pt_name_first'] 
#             pt_last = request.GET['pt_name_last'] 
#             family_name = request.GET['family_member_name'] 
#             family_email = request.GET['family_email']
#             relation = request.GET['family_relation']
#             pt_room = request.GET['pt_room']
#             pt_hospital = request.GET['pt_hospital']
#             context = {'pt_name_first':pt_first,
#                        'pt_name_last': pt_last,
#                        'family_member_name':family_name,
#                        'family_email': family_email,
#                        'family_relation':relation,
#                        'pt_room':pt_room,
#                        'pt_hospital': pt_hospital,
#                       }
                        
#             if not q1:
#                 new_uuid = uuid.uuid4()
#                 new_pt = Benefactor(
#                     first_name=pt_first,
#                     last_name=pt_last,
#                     room_number=pt_room,
#                     hospital_name=pt_hospital,
#                     verification_code=new_uuid
#                     )
#                 new_pt.save()
#                 context['benefactor'] = new_pt

#             return HttpResponse(template2.render(context, request))
#         else:
#             form = VolunteerUploadForm()     

#     return render(
#         request, 
#         'geri_app/pt_upload.html',
#         {'form': form}
#     )

#TODO Make the email upload async so it's faster? 
@group_required('volunteer')
def pt_upload_success(request):
    email = request.GET['email']
    name = request.GET['name']
    code = request.GET['code']
    fname = request.GET['pt_first']
    lname = request.GET['pt_last']

    context = {
        "email":email,
        'name':name,
        'code':code,
        'fname':fname,
        'lname':lname
    }

    full_name = fname + " " + lname
    upload_link = "http://" + request.get_host() +"/verify/?code=" + str(code)

    email_body_text = "Dear" + name + ",\nWelcome to Curami! Thank you for taking the first step toward your Curami experience. Using Curami, you can send personalized video messages to your loved ones in the hospital at any time of the day from anywhere in the world. \nClick on this link to share your love with "+ full_name +" by sending them a video. \n Know any other family or friends who would like to share their love and send a message to " + full_name +"? Send them this link to upload a video: "+ upload_link + ". \nIf you have any questions, please reach out to the Curami Team at TeamCurami@gmail.com. \nBest wishes,\n The Curami Team"

    email_link_href = r'<a href="' + upload_link + '">' + upload_link + "</a>"
    print 'upload_link' , upload_link
    print email_link_href
    email_body_html = """
        <html>
          <head></head>
          <body>
               Dear """ + name + """,<br /><br />
               Welcome to Curami! Thank you for taking the first step toward your Curami experience. Using Curami, you can send personalized video messages to your loved ones in the hospital at any time of the day from anywhere in the world.<br /><br />
               Click on this link to share your love with """ + full_name + """ by sending them a video.<br /><br />
               Know any other family or friends who would like to share their love and send a message to """+full_name+"""? Send them this link to upload a video: """ + email_link_href+"""</a>.<br /><br />
               If you have any questions, please reach out to the Curami Team at TeamCurami@gmail.com.<br /><br />
               Best wishes,<br />
               The Curami Team
            </p>
          </body>
        </html>
        """

    send_email('teamcurami@gmail.com', "Team Curami",'Curami123', email, 'Here we go!', email_body_text, email_body_html)


    return render(
        request, 
        'geri_app/patient_upload_success.html',
        context,
    )

@group_required('volunteer')
def volunteer_landing(request):
    q = Benefactor.objects.filter(
            isCurrentPatient=True
        )
    allVideosByPt = {}
    for patient in q:
        allVideosByPt[patient.id] = {}
        print "patinet: ", patient.id
        #allVideosByPt
        allVideosByPt[patient.id]["pt_info"] = patient
        pt_videos = MediaDocument.objects.filter(
                benefactor=patient,
                hasBeenViewed=False
            )
        allVideosByPt[patient.id]['data'] = pt_videos
        if pt_videos:
            allVideosByPt[patient.id]['has_video'] = True
        else:
            allVideosByPt[patient.id]['has_video'] = False

    context = {}

    print "videos: ", allVideosByPt
    if q:
        context['active_patients'] = allVideosByPt
        template = loader.get_template('geri_app/volunteer_landing.html')

    return render(
        request, 
        'geri_app/volunteer_landing.html',
        context
    )

def pt_find(request):

    try:
        fname = request.GET['pt_fname']
        lname = request.GET['pt_lname']
        pt_room = request.GET['pt_room']
        pt_hospital = request.GET['pt_hospital']
    except MultiValueDictKeyError:
        return HttpResponseRedirect('/patient_search')

    context = {}
    q = Benefactor.objects.filter(
            first_name=fname,
            last_name=lname,
            room_number=pt_room,
            hospital_name=pt_hospital, 
        )

    if q:
        found_patient = q[0]
        context['fname'] = found_patient.first_name
        context['lname'] = found_patient.last_name
        context['room'] = found_patient.room_number
        context['hospital'] = found_patient.hospital_name

        return HttpResponseRedirect('/verify/?code='+str(found_patient.verification_code))

    #     return render(
    #     request, 
    #     'geri_app/pt_find.html',
    #     context
    # )
    else:
        return HttpResponseRedirect('/patient_search')


def send_email(user, team_name, pwd, recipient, subject, text_body, html_body):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = team_name + "<"+user+">"

    part1 = MIMEText(text_body, 'plain')
    part2 = MIMEText(html_body, 'html')

    msg.attach(part1)
    msg.attach(part2)

    FROM = team_name + "<"+user+">"
    TO = recipient if type(recipient) is list else [recipient]
    msg['To'] = ", ".join(TO)

    gmail_user = user
    gmail_pwd = pwd
    
    # TO = recipient if type(recipient) is list else [recipient]
    # SUBJECT = subject
    # TEXT = body

    # Prepare actual message
    #message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, msg.as_string())
        server.quit()
        print 'successfully sent the mail'
    except Exception as inst:
        print inst
        print "failed to send mail"




