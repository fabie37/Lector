from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


app_name = 'lector-app'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('uploads/', views.uploads, name='uploads'),
    path('library/', views.library, name='library'),
    path('details/', views.details, name='details'),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search, name='search'),
    path('book_search/', views.book_search, name='book_search'),
    path('audio_player/', views.audio_player, name='audio_player'),
    path('uploads/', views.recording_form_upload, name='upload'),
    path('list/', views.recordings_list, name='list'),
    path('validate_login/', views.validate_login, name='validate_login'),
    path('validate_signup/', views.validate_signup, name='validate_signup'),
    path('accounts/', include('allauth.urls')),
]


