from django.contrib.auth import logout
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
from .forms import *
from .models import *
from django.template import RequestContext
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone
from reportlab.pdfgen import canvas
from django.utils.html import strip_tags
# from docx import *
# from docx.shared import Inches



def register_confirm(request, activation_key):
    # check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('/home/')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    # check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render_to_response('/accounts/login/')
    # if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('registration/confirm.html')


def register_user(request):
    args = {}

    args.update(csrf(request))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        args['form'] = form

        if form.is_valid():
            form.save()  # save user to database if form is valid
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1((str(random.random())).encode('utf8')).hexdigest()[:5]
            activation_key = hashlib.sha1((salt + email).encode('utf8')).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            print(activation_key, "activation key")
            # Get user by username
            user = User.objects.get(username=username)
            user.is_active = False
            user.save()
            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key,
                                      key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            48hours http://127.0.0.1:8000/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'shubham.namdeo@gmail.com',
                      [email], fail_silently=False)

            return HttpResponseRedirect('/success/')
    else:
        args['form'] = RegistrationForm()

    return render_to_response('registration/register.html', args, context_instance=RequestContext(request))


def register_success(request):
    return render_to_response(
        'registration/success.html',
    )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def home(request):
    return render_to_response(
        'home.html',
        {'user': request.user}
    )

def newnotes(request):
    args = {}
    args.update(csrf(request))

    if request.method == 'POST':
        form = Note.objects.create()
        form.title = request.POST.get('title')
        form.notes = request.POST.get('notes')
        form.logged_user = str(request.user)
        form.dates = datetime.datetime.utcnow().replace(tzinfo=utc)
        form.save()
        user_loggedin = str(request.user)
        my_data = Note.objects.all().filter(logged_user=user_loggedin)
        # print_dates=''
        # print_notes=''
        # print_title=''
        # for j in my_data:
        #     print (j)
        #     if j.logged_user == user_loggedin:
        #         print(j.notes,"sadfsfsdfsfsfd")
        #         print_notes = j.notes
        #         print_title = j.title
        #         print_dates = j.dates
        return render_to_response('notes.html', {'user_loggedin': user_loggedin, 'my_data':my_data},
                                              context_instance=RequestContext(request))

    else:
        user_loggedin = str(request.user)
        my_data = Note.objects.all().filter(logged_user=user_loggedin)
        return render_to_response('notes.html', {'user_loggedin': user_loggedin, 'my_data':my_data},
                                              context_instance=RequestContext(request))



def chats(request):
    args = {}

    args.update(csrf(request))
    if request.method == 'POST':
        form = CommentForm(request.POST.get('commentform'))
        form.comment = request.POST.get('comments')
        form.logged_inuser = request.user
        form.dates = datetime.datetime.utcnow().replace(tzinfo=utc)
        form.save()
        list = []
        for i in CommentForm.objects.all():
            print(i.comment)
            list.append(i.comment)
        my_data = CommentForm.objects.filter().order_by('-id')
        my_users = UserProfile.objects.all()
        user_loggedin = (request.user)


        return render_to_response('chat.html', {'user_loggedin':user_loggedin, 'com': list[-1], 'my_data': my_data, 'my_users': my_users },
                                  context_instance=RequestContext(request))

    else:
        user_loggedin = (request.user)
        my_data = CommentForm.objects.filter().order_by('-id')
        my_users = User.objects.all()


        return render_to_response('chat.html',
                                  {'user_loggedin': user_loggedin,  'my_data': my_data, 'my_users': my_users},
                                  context_instance=RequestContext(request))

def articles(request):
        args = {}

        args.update(csrf(request))
        if request.method == 'POST':
            form = ArtForm(request.POST, request.FILES)
            if form.is_valid():
                form.title = request.POST.get('title')
                form.desc = request.POST.get('description')
                form.docfile = Art(docfile = request.FILES['docfile'])
                form.dates = datetime.datetime.utcnow().replace(tzinfo=utc)
                form.save()

                my_data = Art.objects.all()
                user_loggedin = str(request.user)
                if (user_loggedin != "shubham.namdeo"):
                    return HttpResponseRedirect('/login/')

                return render_to_response('articles.html',{'form': form, 'my_data': my_data}, context_instance=RequestContext(request))


        else:
            user_loggedin = str(request.user)
            my_data = Art.objects.all()
            if (user_loggedin != 'shubham.namdeo'):
                return HttpResponseRedirect('/accounts/login/')

            form = ArtForm()

        return render_to_response('articles.html', { 'form': form, 'my_data': my_data}, context_instance=RequestContext(request))


def docs(request):
    args={}

    args.update(csrf(request))
    # if request.method == "POST":

    # form = WordForm(request.POST)

    if request.method == 'POST' :
        list = Word.objects.create()
        list.texts = request.POST.get('editor1')
        list.dates = datetime.datetime.utcnow().replace(tzinfo=utc)
        list.save()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="new_pdf.pdf"'
        p = canvas.Canvas(response)
        filtered = strip_tags(list.texts)[:-2]
        p.drawString(100, 750, filtered)
        print (list.texts)
        p.showPage()
        p.save()
        return response
    #     document = Document()
    # docx_title="TEST_DOCUMENT.docx"
    # # ---- Cover Letter ----
    # document.add_picture((r'%s/static/images/my-header.png' % (settings.PROJECT_PATH)), width=Inches(4))
    # document.add_paragraph()
    # document.add_paragraph("%s" % date.today().strftime('%B %d, %Y'))
    #
    # document.add_paragraph('Dear Sir or Madam:')
    # document.add_paragraph('We are pleased to help you with your widgets.')
    # document.add_paragraph('Please feel free to contact me for any additional information.')
    # document.add_paragraph('I look forward to assisting you in this project.')
    #
    # document.add_paragraph()
    # document.add_paragraph('Best regards,')
    # document.add_paragraph('Acme Specialist 1]')
    # document.add_page_break()
    #
    # # Prepare document for download
    # # -----------------------------
    # f = StringIO()
    # document.save(f)
    # length = f.tell()
    # f.seek(0)
    # response = HttpResponse(
    #     f.getvalue(),
    #     content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    # )
    # response['Content-Disposition'] = 'attachment; filename=' + docx_title
    # response['Content-Length'] = length
    # return response
        # render_to_response('docx.html', context_instance=RequestContext(request))

    #
    #
    #
    # if form.is_valid():
    #     print ("hi")
    #     form.texts = request.POST.get('editor1')
    #     print ("hi")
    #     print (form.texts)
    #     form.dates = datetime.datetime.utcnow().replace(tzinfo=utc)
    #     form.save()
    #
    #     comm= Word.objects.all()
    #


    else:
        comm= Word.objects.all()
        form = WordForm()
        print ("!@#$%^&*")
        return render_to_response('docx.html',{ "comm": comm, "form": form}, context_instance=RequestContext(request))
