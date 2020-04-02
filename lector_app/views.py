from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import Recording
from lector_app.forms import UserForm, UserProfileForm,RecordingForm


# Create your views here.

def index(request):
    return render(request, 'lector-app/index.html')


def details(request):
    return render(request, 'lector-app/details.html')


def library(request):
    return render(request, 'lector-app/library.html')


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('lector-app:index'))
    else:
        return render(request, 'lector-app/login.html')


def login(request):
    return render(request, 'lector-app/login.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse('lector-app:index'))
    else:
        return render(request, 'lector-app/signup.html')


def book_search(request):
    return render(request, 'lector-app/book_search.html')


def profile(request):
    return render(request, 'lector-app/profile.html')


def search(request):
    return render(request, 'lector-app/search.html')


def audio_player(request):
    return render(request, 'lector-app/audio_player.html')


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
                  'signup.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            errors.append("login_failed")
        elif user is not None:
            validated = True
            auth_login(request,user)

    json = {
        'errors' : errors,
        'success' : validated
    }
    return JsonResponse(json)


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('lector_app:index'))

# #   @login_required
def recording_form_upload(request):
    # if request.method == 'POST' and request.FILES['myfile']:
    #   myfile = request.FILES['myfile']
    #   fs = FileSystemStorage()
    #   filename = fs.save(myfile.name, myfile)
    #   uploaded_file_url = fs.url(filename)
    #   return render(request, 'uploads.html', {
    #             'uploaded_file_url': uploaded_file_url
    #         })
    # return render(request, 'uploads.html')
    if request.method == 'POST':
        form = RecordingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lector')
    else:
        form = RecordingForm()
    return render(request, 'uploads.html', {
        'form': form
    })

def recordings_list(request):
    recordings=Recording.objects.all
    return render(request,"recording_list.html")