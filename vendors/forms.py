from django import forms
from accounts.models import Vendor,Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db import transaction

User=get_user_model()

#vendor registration form
class UserRegisterForm(UserCreationForm):
    address = forms.CharField()
    email= forms.EmailField(required= True)

    class Meta(UserCreationForm.Meta):
        model= User
        fields= ['username','address','email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user= super().save(commit=False)
        user.address= self.cleaned_data.get('address')
        user.email= self.cleaned_data.get('email')
        user.is_vendor = True
        user.save()
        vendor= Vendor.objects.create(user=user)
        vendor.address= self.cleaned_data.get('address')
        vendor.email= self.cleaned_data.get('email')
        vendor.save()
        return user


#customer login form
class LoginForm(forms.Form):
    username= forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class=': 'form-control'
            }
        )
    )

    password= forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class=': 'form-control'
            }
        )
    )

class VendorUpdateForm(forms.ModelForm):
    email= forms.EmailField()
    address = forms.CharField()

    class Meta():
        model= User
        fields= ['username','email','address']

    @transaction.atomic
    def save(self):
        user= super().save(commit=False)
        user.username=self.cleaned_data.get('username')
        email= self.cleaned_data.get('email')
        address= self.cleaned_data.get('address')
        vendor= Vendor.objects.get(user=user)
        vendor.user.username=user.username
        vendor.email=email
        vendor.address=address
        if transaction.commit:
            user.save()
            vendor.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image']

    
        