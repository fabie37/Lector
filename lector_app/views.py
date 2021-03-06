import math
from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import ValidationError, validate_email
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Author, Book, Recording, UserProfile


# Views

def index_view(request):
    return render(request, 'lector-app/index.html')


@login_required
def details(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    uploads = Recording.objects.filter(reader=user_profile).count()
    library = user_profile.library.all().count()

    context = {
        'user_profile': user_profile,
        'uploads': uploads,
        'library': library
    }

    return render(request, 'lector-app/details.html', context)


@login_required
def library_view(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    library = user_profile.library.all()

    return render(request, 'lector-app/library.html', {'library': library})


@login_required
def uploads_view(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    recordings = Recording.objects.filter(reader=user_profile)

    return render(request, 'lector-app/uploads.html', {'recordings': recordings})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('lector-app:index')
    else:
        return render(request, 'lector-app/login.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('lector-app:index')
    else:
        return render(request, 'lector-app/signup.html')


def book_search_view(request):
    return render(request, 'lector-app/book_search.html')


def search_view(request):
    from .models import Recording

    se = Recording.search_engine
    query = request.GET.get('query', '')
    nresults = int(request.GET.get('nresults', 5))

    results = se.search(query, limit=nresults)

    if request.user.is_authenticated:
        user = request.user
        userprofile = UserProfile.objects.get(user=user)
        user_library = userprofile.library.all()
    else:
        user_library = None

    context = {'query': query,
               'hits': [Recording.objects.get(pk=hit[se.pk_name]) for hit in results],
               'has_more': results.scored_length() < len(results),
               'show_more_nresults': nresults + 5,
               'user_library': user_library}
    return render(request, 'lector-app/search.html', context)


def audio_player(request, recording_id):
    recording = get_object_or_404(Recording, pk=recording_id)
    context = {'recording': recording}
    return render(request, 'lector-app/audio_player.html', context)


def validate_signup(request):
    errors = []
    validated = False
    username = request.POST['username']
    email = request.POST['email']
    voice_type = request.POST['voice_type']
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
        except ValidationError:
            errors.append("email_invalid")
    if User.objects.filter(email=email).exists():
        errors.append("email_exists")
    if not voice_type:
        errors.append("voice_type_empty")
    if not password:
        errors.append("password_empty")
    if not password_check:
        errors.append("password_check_empty")
    if password != password_check and password and password_check:
        errors.append("password_match")
    if not errors:
        user = User.objects.create_user(username=username, password=password, email=email)
        UserProfile.objects.create(user=user, voice_type=voice_type)
        validated = True

    json = {
        'errors': errors,
        'success': validated
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
            login(request, user)

    return JsonResponse({
        'errors': errors,
        'success': validated
    })


@login_required
def user_logout(request):
    logout(request)
    return redirect('lector-app:index')


@login_required
def validate_upload_form(request):
    errors = []
    validated = False
    title = request.POST['title']
    author = request.POST['author']
    file_boolean = request.POST['file']

    # Empty fields
    if not title:
        errors.append("title_empty")

    if not author:
        errors.append("author_empty")
    elif len(author.split(" ")) < 2:
        errors.append("author_invalid")

    if file_boolean == 'false':
        errors.append("file_invalid")

    if not errors:
        validated = True

    return JsonResponse({
        'errors': errors,
        'success': validated
    })


@login_required
def validate_upload(request):
    errors = []
    validated = False
    title = request.POST['title']
    author = request.POST['author']
    duration = timedelta(seconds=int(math.floor(float(request.POST['duration']))))
    custom_file = request.FILES['file']

    # Empty fields
    if not title:
        errors.append("title_empty")

    if not author:
        errors.append("author_empty")
    elif len(author.split(" ")) < 2:
        errors.append("author_invalid")

    if not custom_file:
        errors.append("file_empty")

    if not duration:
        errors.append("duration_empty")

    if not errors:
        # Manipluate Data
        names = author.split(" ", 1)
        first = names[0]
        last = names[1]
        first = first.capitalize()
        last = last.capitalize()
        author = Author.objects.get_or_create(first_name=first, last_name=last)
        book = Book.objects.get_or_create(title=title, author=author[0])
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        Recording.objects.get_or_create(book=book[0], reader=user_profile, audio_file=custom_file,
                                        duration=duration)
        validated = True

    return JsonResponse({
        'errors': errors,
        'success': validated
    })


@login_required
def remove_recording(request):
    json = {}

    try:
        recording_id = request.POST['recording_id']
        recording = Recording.objects.filter(pk=recording_id)
        recording.delete()
        json['status'] = "success"
    except:
        json['status'] = "failure"

    return JsonResponse(json)


@login_required
def add_library(request):
    json = {}

    state = request.POST['state']

    if state == "add":
        recording_id = request.POST['recording_id']
        recording = Recording.objects.get(pk=recording_id)
        user = request.user
        userprofile = UserProfile.objects.get(user=user)
        userprofile.library.add(recording)
        json['state'] = "added"
    elif state == "remove":
        recording_id = request.POST['recording_id']
        recording = Recording.objects.get(pk=recording_id)
        user = request.user
        userprofile = UserProfile.objects.get(user=user)
        userprofile.library.remove(recording)
        json['state'] = "removed"

    return JsonResponse(json)


@login_required
def remove_library(request):
    json = {}

    try:
        recording_id = request.POST['recording_id']
        recording = Recording.objects.get(pk=recording_id)
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        user_profile.library.remove(recording)
        json['status'] = "success"
    except:
        json['status'] = "failure"

    return JsonResponse(json)
