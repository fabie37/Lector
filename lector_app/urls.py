from django.urls import path

from . import views


app_name = 'lector-app'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('uploads/', views.uploads_view, name='uploads'),
    path('library/', views.library_view, name='library'),
    path('details/', views.details, name='details'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('search/', views.search_view, name='search'),
    path('book_search/', views.book_search_view, name='book_search'),
    path('audio_player/<int:recording_id>', views.audio_player, name='audio_player'),
    path('validate_login/', views.validate_login, name='validate_login'),
    path('validate_upload/', views.validate_upload, name='validate_upload'),
    path('validate_upload_form/', views.validate_upload_form, name='validate_upload_form'),
    path('remove_recording/', views.remove_recording, name='remove_recording'),
    path('add_library/', views.add_library, name='add_library'),
    path('remove_library/', views.remove_library, name='remove_library'),
]
