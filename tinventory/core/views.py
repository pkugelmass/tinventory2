from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from tinventory.core.forms import SignUpForm
from stronghold.decorators import public
from django.core.mail import send_mail

def notify_paul(user):
    new_user_string = "%s (%s)" % (user.get_full_name(), user.username)
    send_mail(
        '[Tinventory] New Signup - %s.' % (new_user_string),
        'A new user - %s has signed up.' % (new_user_string),
        'tinventory900@gmail.com',
        ['paul.kugelmass@ontario.ca'],
        fail_silently=True,
        )

@public
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            notify_paul(user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})