from users.forms import UserProfileInfoForm, UserForm
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'users/index.html')

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'users/userLogin.html', {
        'message': "Logged out."
    })

@login_required
def special(request):
    return HttpResponse('You are logged in, Nice')


def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'users/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })


def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

    
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    

        else:
            print('Login Failed')
            print(f"Username: {username}\nPassword: {password}")
            return render(request, 'users/userLogin.html', {
                'message': 'Invalid Credentials.'
            })
    else:
        return render(request, 'users/userLogin.html', {
        })
   