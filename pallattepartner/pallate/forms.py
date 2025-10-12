from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    email = forms.EmailField(max_length=254, required=True, label="Email Address")

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
            field.widget.attrs.update({
                'class': base_classes,
                'placeholder': field.label,
            })

        # Password field adjustments for readability
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})