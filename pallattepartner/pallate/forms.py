from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=True)
	last_name = forms.CharField(max_length=30, required=True)
	email = forms.EmailField(max_length=254, required=True)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def save(self, commit=True):
		user = super().save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		base_classes = "w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple"
		for field_name, field in self.fields.items():
			# apply classes to all inputs
			field.widget.attrs.update({
				'class': base_classes,
				'placeholder': field.label,
			})
