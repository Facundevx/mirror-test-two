"""Definimos las urls para los users"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'users'
urlpatterns = [
    #Login page
    path('login/',
         auth_views.LoginView.as_view(template_name='users/login.html'),
         name='login'),
    #Log out page
    path('logout/',
         auth_views.LogoutView.as_view(), name='logout'),

    path('register/', views.register, name='register'),

]