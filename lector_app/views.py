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


def uploads(request):
    return render(request, 'lector-app/uploads.html')


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('lector-app:index'))
    else:
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


def validate_signup(request):
    errors = []
    validated = False
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password_check = request.POST['password_check']
    # Empty fields
    if not username:
        errors.append("username_empty")
    elif User.objects.filter(username=username).exists():
        errors.append("username_exists")
    if not email:
        errors.append("email_empty")
    else:
        try:
            validate_email(email)
        except:
            errors.append("email_invalid")
    if User.objects.filter(email=email).exists():
        errors.append("email_exists")
    if not password:
        errors.append("password_empty")
    if not password_check:
        errors.append("password_check_empty")
    if password != password_check and password and password_check:
        errors.append("password_match")
    if not errors:
        user = User.objects.create_user(username=username, password=password, email=email)
        validated = True
    
    json = {
        'errors' : errors,
        'success' : validated
    }
    return JsonResponse(json)

    # Authenticate User
    if username and password:
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

def validate_login(request):
    errors = []
    validated = False
    username = request.POST['username']
    password = request.POST['password']
    # Empty fields
    if not username:
        errors.append("username_empty")
    if not password:
        errors.append("password_empty")
    # Authenticate User
    if username and password:
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
    return redirect(reverse('lector-app:index'))

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