from django.contrib import admin
from django.urls import path

from account.views import (
	home_screen_view,
    registration_view,
    logout_view,
    login_view,
    change_password_view,
    change_username_view,
)

#anytime a new route is created, it must be added here
urlpatterns = [
    path('', home_screen_view, name="homepage"),
    path('signup/', registration_view, name="signup"),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('change_password/', change_password_view, name="change_password"),
    path('change_username/', change_username_view, name="change_username"),
]
