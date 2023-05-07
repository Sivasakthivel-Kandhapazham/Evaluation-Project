from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_view, name="login"),
    path('register', views.register_view, name='register'),
    path('user_registration', views.user_registration, name='user_registration'),
    path('authenticate_user', views.authenticate_user, name='authenticate_user'),
]