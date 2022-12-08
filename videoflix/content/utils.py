from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage

# log_in utils:

def authenticate_user_from_form(form):
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')
    user = authenticate(username = username, password = password)
    
    return user


def success_response_after_login(request, redirection = ""):
    if redirection:
        messages.success(request, "You have successfully logged in!")
        print('hiii')

        return redirect(request.POST.get('next'))

    else:
        messages.success(request, "You have successfully logged in!")
        print('heee')
        response = redirect('/home/')
    
        return response


def error_response_after_login_attempt(request):
    messages.error(request, "You have entered an invalid username or password.")
    storage = get_messages(request)

    return render(request, 'auth/login.html', {'messages': storage})


# sign_up and activate_user utils:

def send_email(request, user, email):
    email_subject = 'Activate your user'
    email_body = render_to_string('auth/activate-user-email.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    whole_email = EmailMessage(email_subject, email_body, to = [email])

    if whole_email.send():
        messages.warning(request, 'Confirmation email was sent to "{}". Please click on the link inside to activate your user and finish the signup process.'.format(email))

    else:
        messages.error('It was not possible to send an email to "{}"'.format(email))


def success_response_after_signup(request):
    messages.success(request, "You have successfully signed up!")
    storage = get_messages(request)

    return render(request, 'videoflix/home.html', {'messages': storage})


def error_response_after_activation_link_expires(request):
    messages.error(request, "The activation link has expired. Please repeat the whole process from the beginning.")
    storage = get_messages(request)

    return render(request, 'auth/login.html', {'messages': storage})


def error_response_after_signup_attempt(request, errors):
    for error in errors:
        if error == 'username':
                messages.error(request, "Unfortunately this username is already in use.")

        elif error == 'email':
                 messages.error(request, "Please check the email format. It's not correct.")

        else:
            messages.error(request, "Please remember that your password has to be the same in both fields.")

        storage = get_messages(request)

        return render(request, 'auth/signup.html', {'messages': storage})


# activate_user utils:

def find_encrypted_user(user_model, uidb64):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user_model.objects.get(pk = uid)

        return user
    
    except:
        user = None

        return None