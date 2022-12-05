from django.shortcuts import render, redirect
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_page
from .forms import NewUserForm, NewVideoForm, EditVideoForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Video
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.messages import get_messages

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your views here.

def redirect_to_home(request):

    response = redirect('/home/')
    
    return response

def log_in(request):

    redirect = request.GET.get('next')
    
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)

            if user is not None:
                login(request, user)

                if redirect:
                    messages.success(request, "You have successfully logged in!")

                    return HttpResponseRedirect(request.POST.get('next'))

                else:
                    messages.success(request, "You have successfully logged in!")

                    return redirect_to_home(request)

            else:
                messages.error(request, "You have entered an invalid username or password.")
                storage = get_messages(request)

                return render(request, 'auth/login.html', {'messages': storage})
        else:
            messages.error(request, "You have entered an invalid username or password.")
            storage = get_messages(request)

            return render(request, 'auth/login.html', {'messages': storage})

    form = AuthenticationForm()

    return render(request, 'auth/login.html', {'redirect': redirect})

def sign_up(request):

    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit = False)
            user.is_active = False
            user.save()
            send_email(request, user, form.cleaned_data.get('email'))
            form = NewUserForm()
            storage = get_messages(request)

            return render(request, 'auth/signup.html', {'messages': storage})
        
        else:

            for error in form.errors:

                if error == 'username':
                    messages.error(request, "Unfortunately this username is already in use.")

                elif error == 'email':
                    messages.error(request, "Please check the email format. It's not correct.")

                else:
                    messages.error(request, "Please remember that your password has to be the same in both fields.")

                storage = get_messages(request)

                return render(request, 'auth/signup.html', {'messages': storage})

    form = NewUserForm()
    
    return render(request, 'auth/signup.html')

def send_email(request, user, to_email):

    email_subject = 'Activate your user'
    email_body = render_to_string('auth/activate-user-email.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    whole_email = EmailMessage(email_subject, email_body, to = [to_email])

    if whole_email.send():
        messages.warning(request, 'Confirmation email was sent to "{}". Please click on the link inside to activate your user and finish the signup process.'.format(to_email))

    else:
        messages.error('It was not possible to send an email to "{}"'.format(to_email))

def activate_user(request, uidb64, token):

    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
    
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "You have successfully signed up!")
        storage = get_messages(request)

        return render(request, 'videoflix/home.html', {'messages': storage})
    
    else:
        messages.error(request, "The activation link has expired. Please repeat the whole process from the beginning.")
        storage = get_messages(request)

        return render(request, 'auth/login.html', {'messages': storage})

@login_required(login_url = '/login/')
def home(request):

    videos = Video.objects.filter(creator = request.user) 
    
    return render(request, 'videoflix/home.html', {'videos': videos})

@login_required(login_url = '/login/')
def create_video(request):

    if request.method == "POST":
        form = NewVideoForm(request.POST, request.FILES)
        
        if form.is_valid():
            instance = form.save(commit = False)
            instance.creator = request.user
            instance.save()
            form = NewVideoForm()
            messages.success(request, "You have successfully added a video!")

            return redirect_to_home(request)

    form = NewVideoForm()

    return render(request, 'videoflix/create-video.html')

@login_required(login_url = '/login/')
def see_video_details(request, pk):

    video_to_display = Video.objects.get(pk = pk)

    return render(request, 'videoflix/video-details.html', {'video': video_to_display})

@login_required(login_url = '/login/')
def edit_video(request, pk):

    video_to_edit = Video.objects.get(pk = pk)

    if request.method == "POST":
        form = EditVideoForm(request.POST)

        if form.is_valid():
            video_to_edit.title = form.cleaned_data.get('title')
            video_to_edit.description = form.cleaned_data.get('description')
            video_to_edit.save()
            form = EditVideoForm()
            messages.success(request, "You have successfully edited the video!")
            
            return redirect_to_home(request)

        else:
            messages.error(request, "Video could not be edited. Please try it again.")
            storage = get_messages(request)

            return render(request, 'videoflix/edit-video.html', {'video': video_to_edit, 'messages': storage})

    form = EditVideoForm()

    return render(request, 'videoflix/edit-video.html', {'video': video_to_edit})

@login_required(login_url = '/login/')
def delete_video(request, pk):

    video_to_delete = Video.objects.get(pk = pk)

    if request.method == "POST":
        video_to_delete.delete()
        messages.success(request, 'You have successfully deleted the video "{}"!'.format(video_to_delete.title))

        return redirect_to_home(request)

    return render(request, 'videoflix/delete-video.html', {'video': video_to_delete})

def log_out(request):
     
    logout(request)
    messages.success(request, "You have successfully logged out. See you soon!")

    return redirect_to_home(request)
