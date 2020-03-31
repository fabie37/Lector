import importlib
lector_app = importlib.import_module("lector_app.views")

from django.urls import path
from lector_app import views
app_name = 'lector_app'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    ]