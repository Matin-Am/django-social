from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"enter username","class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"enter password","class":"form-control"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"placeholder":"enter email","class":"form-control"}))
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("This email already  exists")
        return email


    



class LoginUserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"enter username","class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"enter password","class":"form-control"}))




class EditUserForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = Profile
        fields = ("age","bio",)
