from django.contrib import admin
from django.urls import path

from account.views import (
	home_screen_view,
    registration_view,
    logout_view,
    login_view,
)

#anytime a new route is created, it must be added here
urlpatterns = [
    path('', home_screen_view, name="homepage"),
    path('register/', registration_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
]
