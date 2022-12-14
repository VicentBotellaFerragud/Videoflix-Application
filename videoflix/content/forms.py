from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Video, Rating

# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required = True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2",)

	def save(self, commit = True):
		user = super(NewUserForm, self).save(commit = False)
		user.email = self.cleaned_data['email']

		if commit:
			user.save()

		return user


class EditUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ("username",)


class NewVideoForm(forms.ModelForm):
	class Meta:
		model = Video
		fields = ("category", "title", "description", "video_file",)


class EditVideoForm(forms.ModelForm):
	class Meta:
		model = Video
		fields = ("category", "title", "description",)


class RateVideoForm(forms.ModelForm):
	class Meta:
		model = Rating
		fields = ("rating",)
