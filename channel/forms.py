# from django.contrib.auth.models import User
from django import forms
from .models import User

class UserForm(forms.ModelForm):
    email = forms.CharField(widget= forms.EmailInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    first_name = forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Name'}))
    class Meta:
        model = User
        fields = ['first_name','email', 'password']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

class PasswordForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=('password',)

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password =self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords does not match"
)