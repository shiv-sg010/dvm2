from django import forms
from accounts.models import Customer,Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import CartItems

User=get_user_model()

#customer registration form
class UserRegisterForm(UserCreationForm):
    address = forms.CharField()
    email= forms.EmailField(required= True)

    class Meta():
        model= User
        fields= ['username','address','email', 'password1', 'password2',]

    @transaction.atomic
    def save(self):
        user= super().save(commit=False)
        user.address= self.cleaned_data.get('address')
        user.email= self.cleaned_data.get('email')
        user.is_customer = True
        user.save()
        customer= Customer.objects.create(user=user)
        customer.address=self.cleaned_data.get('address')
        customer.email=self.cleaned_data.get('email')
        customer.save()
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

class CustomerUpdateForm(forms.ModelForm):
    email= forms.EmailField()
    address = forms.CharField()
    amount=forms.FloatField(required=True)

    class Meta():
        model= User
        fields= ['username','email','address', 'amount']

    @transaction.atomic
    def save(self):
        user= super().save(commit=False)
        user.username=self.cleaned_data.get('username')
        email= self.cleaned_data.get('email')
        address= self.cleaned_data.get('address')
        amount= self.cleaned_data.get('amount')
        customer= Customer.objects.get(user=user)
        customer.user.username=user.username
        customer.email=email
        customer.address=address
        customer.amount=amount
        if transaction.commit:
            user.save()
            customer.save()
        return user


    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image']
        