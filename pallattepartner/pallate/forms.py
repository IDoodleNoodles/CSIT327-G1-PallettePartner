from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Collaboration, Profile, Artwork, Message

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

        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})


class CollaborationForm(forms.ModelForm):
    class Meta:
        model = Collaboration
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Project Title',
                'class': 'input-field'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe your project...',
                'class': 'textarea-field',
                'rows': 4
            })
        }


class ProfileForm(forms.ModelForm):
    # Add User model fields
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'email@example.com',
            'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name',
            'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
        }),
        label='First Name'
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name',
            'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
        }),
        label='Last Name'
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Leave blank to keep current password',
            'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
        }),
        help_text='Leave blank if you don\'t want to change your password'
    )
    password_confirm = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm new password',
            'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
        }),
        label='Confirm Password'
    )
    
    class Meta:
        model = Profile
        fields = ['avatar', 'art_type', 'portfolio', 'bio']
        
        # Reusable CSS class for input fields
        input_class = 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
        
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-200 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-accent-purple file:text-white hover:file:bg-purple-600',
                'accept': 'image/*'
            }),
            'art_type': forms.TextInput(attrs={
                'placeholder': 'e.g., Digital Artist, Illustrator, Photographer',
                'class': input_class
            }),
            'portfolio': forms.URLInput(attrs={
                'placeholder': 'https://your-portfolio.com',
                'class': input_class
            }),
            'bio': forms.Textarea(attrs={
                'placeholder': 'Tell us about yourself...',
                'class': input_class,
                'rows': 4
            })
        }
        labels = {
            'avatar': 'Profile Picture',
            'art_type': 'Art Type',
            'portfolio': 'Portfolio URL',
            'bio': 'Bio'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(pk=self.instance.user.pk).filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.user.pk).filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password != password_confirm:
            raise forms.ValidationError('Passwords do not match.')
        
        return cleaned_data
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        
        # Update User model fields
        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        
        # Update password if provided
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
            profile.save()
        
        return profile


class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Artwork Title',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe your artwork...',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple',
                'rows': 4
            }),
            'image': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-200 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-accent-purple file:text-white hover:file:bg-purple-600',
                'accept': 'image/*'
            })
        }
        labels = {
            'title': 'Title',
            'description': 'Description',
            'image': 'Upload Image'
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Type your message...',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple',
                'rows': 3
            })
        }
        labels = {
            'text': 'Message'
        }