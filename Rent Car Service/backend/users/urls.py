from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('users/register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('users/profile/', views.UserDetailView.as_view(), name='user-profile'),
    path('users/login/', views.user_login, name='user-login'),
    path('users/logout/', views.user_logout, name='user-logout'),
]
