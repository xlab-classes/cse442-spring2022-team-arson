from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import Account
from account.forms import (
	RegistrationForm,
	AccountAuthenticationForm,
	ChangeUsernameForm,
)


def home_screen_view(request):
	context = {}

	accounts = Account.objects.all()
	context["accounts"] = accounts

	return render(request, "account/home.html", context)

###########################################################
def registration_view(request):
	context = {}

	if request.POST:
		form = RegistrationForm(request.POST)

		# if valid signup credentials, save user to DB, login, and redirect
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			account = authenticate(username=username, password=password)
			login(request, account)
			return redirect("homepage")
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/signup.html', context)


###########################################################
def login_view(request):
	context = {}

	user = request.user

	# if already logged in, redirect to homepage
	if user.is_authenticated:
		return redirect("homepage")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)

		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username,password=password)

			if user:
				login(request, user)
				return redirect("homepage")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form
	return render(request, 'account/login.html', context)

###########################################################
@login_required
def logout_view(request):
	logout(request)
	return redirect("homepage")        

###########################################################
@login_required
def change_password_view(request):
	context = {}

	if request.POST:
		p_form = PasswordChangeForm(request.user, request.POST)
		if p_form.is_valid():
			user = p_form.save()
			update_session_auth_hash(request, user) #keep user logged in after update
			messages.success(request, 'Your password was successfully updated!')
			return redirect('homepage')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		p_form = PasswordChangeForm(request.user)

	context["p_form"] = p_form
	return render(request, 'account/change_password.html', context)
###########################################################
# @login_required
def change_username_view(request):
	context = {}

	if request.POST:
		u_form = ChangeUsernameForm(request.POST, instance=request.user)
		
		if u_form.is_valid():
			user = u_form.save()
			messages.success(request, 'Your username was successfully updated!')
			return redirect('homepage')
		
		else:
			messages.error(request, 'Please correct the error below.')
			return redirect('login')
	else:
		u_form = ChangeUsernameForm(instance=request.user)
		context["u_form"] = u_form
		return render(request, 'account/change_username.html', context)

    
 # create DB in MySQL
 # edit DATABASES in settings.py to support MySQL instead of SQLite
 # could use path/to/my.{ini|cnf} to hide DB password in settings.py