from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from lector_app.forms import UserForm, UserProfileForm,RecordingForm


# Create your views here.

def index(request):
    return render(request, 'lector-app/index.html')

def homepage(request):
    return HttpResponse('homepage')

def signup(request):
    return render(request, 'lector-app/signup.html')

def details(request):
    return render(request, 'lector-app/details.html')

def library(request):
    return render(request, 'lector-app/library.html')

def uploads(request):
    return render(request, 'lector-app/uploads.html')

def login(request):
    return render(request, 'lector-app/login.html')

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
                  'lector_app/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('lector-app:register'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Inavlid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'lector_app/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('lector-app:login'))

#   @login_required
def recording_form_upload(request):
    if request.method == 'POST':
        form = RecordingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lector/')
    else:
        form = RecordingForm()
    return render(request,'recording_upload.html', {
        'form': form
    })
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['Recording']
        fs = FileSystemStorage()
        name = fs.save(str(uploaded_file), uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)
