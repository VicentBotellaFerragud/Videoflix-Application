from django.contrib.auth import authenticate

def authenticate_user_from_form(form):
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')
    user = authenticate(username = username, password = password)
    
    return user