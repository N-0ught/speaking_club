from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import ProfileModel, CommentsModel


class Registration(UserCreationForm):
    email = forms.EmailField(label='Your email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    def __init__(self, *args, **kwargs):
        super(Registration, self).__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'Username'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Password confirmation'})
        for field in ('username', 'email', 'password1', 'password2'):
            self.fields[field].label = None

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(Registration, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class EditForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        exclude = ['slug', 'user']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full name'}),
            'telegram': forms.TextInput(attrs={'placeholder': 'Telegram'}),
            # 'language': forms.Select(attrs={'margin-left:20px'}),
            # 'language_level': forms.Select(attrs={'margin-left:20px'}),
            # 'age': forms.Select(attrs={'margin-left:20px'})
        }


class ResetPassword(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget = forms.EmailInput(attrs={'placeholder': 'Email'})


class ConfirmResetPassword(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(ConfirmResetPassword, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'placeholder': 'New Password'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Password confirmation'})


class ContactUs(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full name'}), max_length=100)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}), max_length=100)
    message = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Your message"}), max_length=1000)


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentsModel
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Your comment goes here...'})
        }