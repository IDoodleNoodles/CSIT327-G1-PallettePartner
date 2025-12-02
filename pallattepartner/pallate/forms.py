from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from .models import (
    Collaboration, Profile, Artwork, Message, ArtworkComment, 
    CollaborationFeedback, CollaborationRole, CollaborationApplication,
    CollaborationFile, CollaborationTask
)

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
        fields = ['title', 'description', 'project_type', 'tags', 'requirements', 'deadline', 'budget']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Project Title',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe your project in detail...',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple',
                'rows': 4
            }),
            'project_type': forms.TextInput(attrs={
                'placeholder': 'e.g., Illustration, Book Cover, Fantasy Art',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
            }),
            'tags': forms.TextInput(attrs={
                'placeholder': 'Comma-separated tags (e.g., Fantasy, Book Cover, Digital)',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
            }),
            'requirements': forms.Textarea(attrs={
                'placeholder': 'List project requirements (one per line)',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple',
                'rows': 3
            }),
            'deadline': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
            }),
            'budget': forms.TextInput(attrs={
                'placeholder': 'e.g., $500, Revenue Share, Portfolio Credit',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
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
    
    security_question = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., What was your first pet\'s name?',
            'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
        }),
        label='Security Question (for password recovery)',
        help_text='Set a question only you can answer'
    )
    security_answer = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your answer (case-insensitive)',
            'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
        }),
        label='Security Answer',
        help_text='This will be used to verify your identity if you forget your password'
    )
    
    class Meta:
        model = Profile
        fields = ['avatar', 'art_type', 'portfolio', 'bio', 'interests', 'location', 'hourly_rate', 'years_active', 'availability_status', 'security_question', 'security_answer']
        
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
            }),
            'interests': forms.Textarea(attrs={
                'placeholder': 'e.g., Fantasy Art, Portraits, Digital Painting, Character Design',
                'class': input_class,
                'rows': 3
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'e.g., San Francisco, CA',
                'class': input_class
            }),
            'hourly_rate': forms.TextInput(attrs={
                'placeholder': 'e.g., $50-150/hour',
                'class': input_class
            }),
            'years_active': forms.NumberInput(attrs={
                'placeholder': 'e.g., 5',
                'class': input_class,
                'min': '0'
            }),
            'availability_status': forms.TextInput(attrs={
                'placeholder': 'e.g., Available for projects',
                'class': input_class
            })
        }
        labels = {
            'avatar': 'Profile Picture',
            'art_type': 'Art Type',
            'portfolio': 'Portfolio URL',
            'bio': 'Bio',
            'interests': 'Interests (comma-separated)',
            'location': 'Location',
            'hourly_rate': 'Hourly Rate',
            'years_active': 'Years Active',
            'availability_status': 'Availability Status'
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

class ArtworkCommentForm(forms.ModelForm):
    class Meta:
        model = ArtworkComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your comment...',
                'class': 'w-full px-3 py-2 rounded-lg bg-[#050819] border border-[#1F2937] text-sm'
            })
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["text", "image"] 

        widgets = {
            "text": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Type your message...",
                "class": "w-full bg-[#111827] text-[#E5E7EB] text-sm rounded-2xl px-4 py-3 border border-[#1F2937] focus:outline-none focus:border-[#8B5CF6]",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "hidden",          
                "accept": "image/*",        
                "id": "id_image",           
            }),
        }


class CollaborationFeedbackForm(forms.ModelForm):
    """Form for submitting feedback/rating for a collaboration"""
    class Meta:
        model = CollaborationFeedback
        fields = ['rating', 'comment']
        
        widgets = {
            'rating': forms.RadioSelect(attrs={
                'class': 'rating-radio'
            }),
            'comment': forms.Textarea(attrs={
                'placeholder': 'Share your collaboration experience...',
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple',
                'rows': 4
            })
        }
        labels = {
            'rating': 'Rate this collaboration',
            'comment': 'Your feedback (optional)'
        }


# Password Reset Forms (No Email Required)
class PasswordResetRequestForm(forms.Form):
    """Step 1: Enter username/email to initiate password reset"""
    username_or_email = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username or email',
            'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
        }),
        label='Username or Email'
    )


class SecurityQuestionAnswerForm(forms.Form):
    """Step 2: Answer security question"""
    security_answer = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your answer',
            'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
        }),
        label='Answer'
    )


class NewPasswordForm(forms.Form):
    """Step 3: Set new password"""
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'New password',
            'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
        }),
        label='New Password',
        help_text='Password must be at least 8 characters'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm new password',
            'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
        }),
        label='Confirm New Password'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Passwords do not match.')
            if len(password1) < 8:
                raise forms.ValidationError('Password must be at least 8 characters.')
        
        return cleaned_data


class CollaborationRoleForm(forms.ModelForm):
    class Meta:
        model = CollaborationRole
        fields = ['title', 'description', 'skills_required', 'compensation', 'time_commitment']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g., Lead Illustrator, Color Specialist',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'What will this role be responsible for?',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple',
                'rows': 3
            }),
            'skills_required': forms.TextInput(attrs={
                'placeholder': 'e.g., Digital Painting, Character Design, Adobe Photoshop',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
            }),
            'compensation': forms.TextInput(attrs={
                'placeholder': 'e.g., $2,800, Revenue Share, Portfolio Credit',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
            }),
            'time_commitment': forms.TextInput(attrs={
                'placeholder': 'e.g., 3 weeks, 1 week, Full cover set',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
            })
        }


class CollaborationApplicationForm(forms.ModelForm):
    class Meta:
        model = CollaborationApplication
        fields = ['message', 'portfolio_link']
        widgets = {
            'message': forms.Textarea(attrs={
                'placeholder': 'Tell us why you\'re interested and share your relevant experience...',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple',
                'rows': 5
            }),
            'portfolio_link': forms.URLInput(attrs={
                'placeholder': 'https://your-portfolio.com (optional)',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
            })
        }


class CollaborationFileForm(forms.ModelForm):
    class Meta:
        model = CollaborationFile
        fields = ['title', 'description', 'file', 'file_type']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'File title',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Optional description',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple',
                'rows': 2
            }),
            'file': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
            }),
            'file_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
            })
        }


class CollaborationTaskForm(forms.ModelForm):
    class Meta:
        model = CollaborationTask
        fields = ['title', 'description', 'assigned_to', 'status', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Task title',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Task details',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple',
                'rows': 3
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 rounded-lg bg-gray-800 text-gray-200 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-accent-purple'
            })
        }
    
    def __init__(self, *args, collaboration=None, **kwargs):
        super().__init__(*args, **kwargs)
        if collaboration:
            # Only show collaboration members in assigned_to dropdown
            members = collaboration.get_members()
            self.fields['assigned_to'].queryset = User.objects.filter(id__in=[m.id for m in members])