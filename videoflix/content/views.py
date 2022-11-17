from django.shortcuts import render, redirect
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_page
from .forms import NewUserForm, NewVideoForm
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

"""
Redirects the user to the home page.
"""
def redirect_to_home(request):

    response = redirect('/home/')
    
    return response

"""
Renders the login view, logs in the user if he/she fulfills the if conditions and redirects him/her either to the home page 
or to the url that he/she has entered.
"""
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
                messages.error(request, "Wrong username or password :(")
                storage = get_messages(request)

                return render(request, 'auth/login.html', {'messages': storage})
        else:
            messages.error(request, "Wrong username or password :(")
            storage = get_messages(request)

            return render(request, 'auth/login.html', {'messages': storage})

    form = AuthenticationForm()

    return render(request, 'auth/login.html', {'redirect': redirect})

"""
Renders the signup view, signs up the user if he/she fulfills the if conditions and redirects him/her to the login page.
"""
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
                    messages.error(request, "Please remember that your password has to meet the conditions and has to be the same in both fields.")

                storage = get_messages(request)

                return render(request, 'auth/signup.html', {'messages': storage})

    form = NewUserForm()
    
    return render(request, 'auth/signup.html')

"""
Sends an email with an activation link (unique for each user) to the passed-in email address.
"""
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

"""
Activates the user so that he/she can use his/her credentials to log in.
"""
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
        messages.success(request, "You have successfully signed up! You can now log in with your credentials :)")
        storage = get_messages(request)

        return render(request, 'auth/login.html', {'messages': storage})
    
    else:
        messages.error(request, "The activation link has expired. Please repeat the whole process from the beginning.")
        storage = get_messages(request)

        return render(request, 'auth/login.html', {'messages': storage})

"""
Renders the home view and stores in the app the videos the user uploads.
"""
@login_required(login_url = '/login/')
# @cache_page(CACHE_TTL) --> This prevents the username from not being updated in the "base.html" file. Why?
def index(request):

    videos = Video.objects.filter(creator = request.user) 

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
    
    return render(request, 'videoflix/index.html', {'videos': videos})

"""
Renders the delete video view and deletes the passed-in video.
"""
@login_required(login_url = '/login/')
def delete_video(request, pk):

    video_to_delete = Video.objects.get(pk = pk)

    if request.method == "POST":
        video_to_delete.delete()
        messages.success(request, 'You have successfully deleted the video "{}"!'.format(video_to_delete.title))

        return redirect_to_home(request)

    return render(request, 'videoflix/delete-video.html', {'video': video_to_delete})

"""
Logs out the user and redirects him/her to the home page.
"""
def log_out(request):
     
    logout(request)
    messages.success(request, "You have successfully logged out. See you soon :)")

    return redirect_to_home(request)
