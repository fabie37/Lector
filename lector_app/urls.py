from django.urls import path

from . import views


app_name = 'lector-app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
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
]
