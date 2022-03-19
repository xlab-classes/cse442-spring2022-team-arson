from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import Account
from django.contrib.auth import authenticate


class RegistrationForm(UserCreationForm):
	username = forms.CharField(max_length=25, help_text="Required. Enter a valid username")

	class Meta:
		model = Account
		fields = ("username", "password1", "password2")


class AccountAuthenticationForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ("username", "password")

	def clean(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			password = self.cleaned_data['password']
			if not authenticate(username=username,password=password):
				raise forms.ValidationError("Invalid Login Credentials")
