from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput

from user.models import *


class SignUp1Form(UserCreationForm):
    username = forms.CharField(max_length=30, label='User Name :',
                               widget=forms.TextInput
                               (attrs={'class': 'form-control', 'style': 'width:500px', 'size': '10',
                                       'required': 'true'}))
    email = forms.EmailField(max_length=200, label='Email :',
                             widget=forms.EmailInput
                             (attrs={'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))
    first_name = forms.CharField(max_length=100, help_text='First Name', label='First Name :',
                                 widget=forms.TextInput
                                 (attrs={'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))
    last_name = forms.CharField(max_length=100, help_text='Last Name', label='Last Name :',
                                widget=forms.TextInput
                                (attrs={'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))
    password1 = forms.CharField(max_length=100, help_text='Password', label='Password :',
                                widget=forms.PasswordInput
                                (attrs={'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))
    password2 = forms.CharField(max_length=100, help_text='Password', label='Password Confirmation :',
                                widget=forms.PasswordInput
                                (attrs={'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)


class SignUp2Form(forms.ModelForm):
    address = forms.CharField(max_length=100, label='Address :',
                              widget=forms.TextInput
                              (attrs={'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))
    city = forms.CharField(max_length=100, label='City :',
                           widget=forms.TextInput
                           (attrs={'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))
    state = forms.CharField(max_length=100, label='State :',
                            widget=forms.TextInput
                            (attrs={'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))
    pin_code = forms.IntegerField(label='Pin Code :',
                                  widget=forms.TextInput
                                  (attrs={'type': 'number', 'class': 'form-control', 'style': 'width:500px',
                                          'required': 'true'}))
    country = forms.CharField(max_length=100, label='Country :',
                              widget=forms.TextInput
                              (attrs={'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))

    class Meta:
        model = User1Profile
        fields = ('address', 'city', 'state', 'pin_code', 'country')


class SignUp3Form(forms.ModelForm):
    phone = forms.IntegerField(label='Phone :',
                               widget=forms.TextInput
                               (attrs={'type': 'number', 'class': 'form-control', 'style': 'width:500px',
                                       'required': 'true'}))

    class Meta:
        model = User2Profile
        fields = ('phone',)


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': TextInput(attrs={'class': 'input', 'placeholder': 'username', 'required': 'true'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'email', 'required': 'true'}),
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'first_name', 'required': 'true'}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'last_name', 'required': 'true'}),
        }


class AddDebitCard(forms.ModelForm):
    dcardnumber = forms.CharField(max_length=16, label='Card Number :',
                                  widget=forms.TextInput
                                  (attrs={'type': 'number', 'class': 'form-control myClass', 'style': 'width:500px',
                                          'name': 'cardnum'}))
    dexpyear = forms.CharField(max_length=4, label='Expiry Year :',
                               widget=forms.TextInput
                               (attrs={'type': 'number', 'max': '2050', 'min': '2021', 'class': 'form-control',
                                       'style': 'width:500px'}))
    dexpmonth = forms.CharField(max_length=2, label='Expiry Month :',
                                widget=forms.TextInput
                                (attrs={'type': 'number', 'max': '13', 'min': '01', 'class': 'form-control',
                                        'style': 'width:500px'}))
    dnameoncard = forms.CharField(max_length=100, label='Name on Card:',
                                  widget=forms.TextInput
                                  (attrs={'class': 'form-control', 'style': 'width:500px'}))
    dcvv = forms.CharField(max_length=3, label='CVV :',
                           widget=forms.TextInput
                           (attrs={'type': 'number', 'class': 'form-control', 'style': 'width:500px'}))

    class Meta:
        model = User4Profile
        fields = ('dcardnumber', 'dexpyear', 'dexpmonth', 'dnameoncard', 'dcvv')

class AddCreditCard(forms.ModelForm):
    ccardnumber = forms.CharField(max_length=16, label='Card Number :',
                              widget=forms.TextInput
                              (attrs={'type':'number', 'class': 'form-control', 'style': 'width:500px'}))
    cexpyear = forms.CharField(max_length=4, label='Expiry Year :',
                           widget=forms.TextInput
                           (attrs={'type':'number', 'max':'2050', 'min':'2021', 'class': 'form-control', 'style': 'width:500px'}))
    cexpmonth = forms.CharField(max_length=2, label='Expiry Month :',
                            widget=forms.TextInput
                            (attrs={'type':'number', 'max':'13', 'min':'01', 'class': 'form-control', 'style': 'width:500px'}))
    cnameoncard = forms.CharField(max_length=100, label='Name on Card:',
                                  widget=forms.TextInput
                                  (attrs={'class': 'form-control', 'style': 'width:500px'}))
    ccvv = forms.CharField(max_length=3, label='CVV :',
                              widget=forms.TextInput
                              (attrs={'type':'number', 'class': 'form-control', 'style': 'width:500px'}))

    class Meta:
        model = User3Profile
        fields = ('ccardnumber', 'cexpyear', 'cexpmonth', 'cnameoncard', 'ccvv')

class AddUpiid(forms.ModelForm):
    upiid = forms.CharField(max_length=100, label='UPI ID :',
                              widget=forms.TextInput
                              (attrs={'class': 'form-control', 'style': 'width:500px'}))

    class Meta:
        model = User5Profile
        fields = ('upiid',)

class AddPaytmno(forms.ModelForm):
    paytmnumber = forms.CharField(max_length=10, label='Paytm linked Number :',
                              widget=forms.TextInput
                              (attrs={'type':'number', 'class': 'form-control', 'style': 'width:500px'}))

    class Meta:
        model = User6Profile
        fields = ('paytmnumber',)

class PhoneForm(forms.ModelForm):
    phone = forms.IntegerField(label='Phone :',
                               widget=forms.TextInput
                               (attrs={'class': 'form-control', 'style': 'width:500px'}))

    class Meta:
        model = User2Profile
        fields = ('phone',)

class AddressForm(forms.ModelForm):
    address = forms.CharField(max_length=100, label='Address :',
                              widget=forms.TextInput
                              (attrs={'class': 'form-control', 'style': 'width:500px'}))
    city = forms.CharField(max_length=100, label='City :',
                           widget=forms.TextInput
                           (attrs={'class': 'form-control', 'style': 'width:500px'}))
    state = forms.CharField(max_length=100, label='State :',
                            widget=forms.TextInput
                            (attrs={'class': 'form-control', 'style': 'width:500px'}))
    pin_code = forms.IntegerField(label='Pin Code :',
                                  widget=forms.TextInput
                                  (attrs={'class': 'form-control', 'style': 'width:500px'}))
    country = forms.CharField(max_length=100, label='Country :',
                              widget=forms.TextInput
                              (attrs={'class': 'form-control', 'style': 'width:500px'}))

    class Meta:
        model = User1Profile
        fields = ('address', 'city', 'state', 'pin_code', 'country')