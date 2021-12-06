from django.urls import path,include
from django.conf.urls import url
from Profile.views import *
from django.contrib.auth import views as auth_view


urlpatterns = [
    url('home',home),
    url('new_registration',new_registration),
    url('registration',registration),
    url('search_user',search_user),
    url('login_user_profile',login_user_profile),
    url('change_profile',change_profile),
    url('call_password',call_password),
    url('call_profile',call_profile),
    url('password_change',password_change),
    url(r'',home),
]
