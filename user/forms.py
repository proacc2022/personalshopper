from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput

from user.models import *


class SignUp1Form(UserCreationForm):
    username = forms.CharField(max_length=30, label='User Name :',
                               widget=forms.TextInput
                               (attrs={'class': 'form-control', 'style': 'width:500px', 'size': '10',
                                       'required': ''}))
    email = forms.EmailField(max_length=200, label='Email :',
                             widget=forms.EmailInput
                             (attrs={'class': 'form-control', 'style': 'width:500px', 'required': ''}))
    first_name = forms.CharField(max_length=100, help_text='First Name', label='First Name :',
                                 widget=forms.TextInput
                                 (attrs={'class': 'form-control', 'style': 'width:500px', 'required': ''}))
    last_name = forms.CharField(max_length=100, help_text='Last Name', label='Last Name :',
                                widget=forms.TextInput
                                (attrs={'class': 'form-control', 'style': 'width:500px', 'required': ''}))
    password1 = forms.CharField(max_length=100, help_text='Password', label='Password :',
                                widget=forms.PasswordInput
                                (attrs={'class': 'form-control', 'style': 'width:500px', 'required': ''}))
    password2 = forms.CharField(max_length=100, help_text='Password', label='Password Confirmation :',
                                widget=forms.PasswordInput
                                (attrs={'class': 'form-control', 'style': 'width:500px', 'required': ''}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)


class SignUp2Form(forms.ModelForm):
    address = forms.CharField(max_length=100, label='Address :',
                              widget=forms.TextInput
                              (attrs={'class': 'form-control', 'style': 'width:500px', 'required': ''}))
    city = forms.CharField(max_length=100, label='City :',
                           widget=forms.TextInput
                           (attrs={'class': 'form-control', 'style': 'width:500px', 'required': ''}))
    state = forms.CharField(max_length=100, label='State :',
                            widget=forms.TextInput
                            (attrs={'class': 'form-control', 'style': 'width:500px', 'required': ''}))
    pin_code = forms.IntegerField(label='Pin Code :',
                                  widget=forms.TextInput
                                  (attrs={'type': 'number', 'class': 'form-control', 'style': 'width:500px',
                                          'required': ''}))
    country = forms.CharField(max_length=100, label='Country :',
                              widget=forms.TextInput
                              (attrs={'class': 'form-control', 'style': 'width:500px', 'required': ''}))

    class Meta:
        model = User1Profile
        fields = ('address', 'city', 'state', 'pin_code', 'country')


class SignUp3Form(forms.ModelForm):
    phone = forms.IntegerField(label='Phone :',
                               widget=forms.TextInput
                               (attrs={'type': 'number', 'class': 'form-control', 'style': 'width:500px',
                                       'required': ''}))

    class Meta:
        model = User2Profile
        fields = ('phone',)


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': TextInput(attrs={'class': 'input form-control', 'placeholder': 'username', 'required': '',
                                         'onkeyup': "javascript:yesnoCheck()"}),
            'email': EmailInput(attrs={'type': 'email', 'class': 'input form-control', 'placeholder': 'email', 'required': '',
                                       'onkeyup': "javascript:yesnoCheck()"}),
            'first_name': TextInput(attrs={'class': 'input', 'placeholder form-control': 'first_name', 'required': '',
                                           'onkeyup': "javascript:yesnoCheck()"}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder form-control': 'last_name', 'required': '',
                                          'onkeyup': "javascript:yesnoCheck()"}),
        }


class AddDebitCard(forms.ModelForm):
    dcardnumber = forms.CharField(max_length=16, label='Card Number :',
                                  widget=forms.TextInput
                                  (attrs={'type': 'number', 'class': 'form-control', 'style': 'width:500px',
                                          'onkeyup': "javascript:yesnoCheck()"}))
    dexpyear = forms.CharField(max_length=4, label='Expiry Year :',
                               widget=forms.TextInput
                               (attrs={'type': 'number', 'max': '2050', 'min': '2021', 'class': 'form-control',
                                       'style': 'width:500px', 'onkeyup': "javascript:yesnoCheck()"}))
    dexpmonth = forms.CharField(max_length=2, label='Expiry Month :',
                                widget=forms.TextInput
                                (attrs={'type': 'number', 'max': '13', 'min': '01', 'class': 'form-control',
                                        'style': 'width:500px', 'onkeyup': "javascript:yesnoCheck()"}))
    dnameoncard = forms.CharField(max_length=100, label='Name on Card:',
                                  widget=forms.TextInput
                                  (attrs={'class': 'form-control', 'style': 'width:500px',
                                          'onkeyup': "javascript:yesnoCheck()"}))
    dcvv = forms.CharField(max_length=3, label='CVV :',
                           widget=forms.TextInput
                           (attrs={'type': 'number', 'class': 'form-control', 'style': 'width:500px',
                                   'onkeyup': "javascript:yesnoCheck()"}))

    class Meta:
        model = User4Profile
        fields = ('dcardnumber', 'dexpyear', 'dexpmonth', 'dnameoncard', 'dcvv')


class AddCreditCard(forms.ModelForm):
    ccardnumber = forms.CharField(max_length=16, label='Card Number :',
                                  widget=forms.TextInput
                                  (attrs={'type': 'number', 'class': 'form-control', 'style': 'width:500px',
                                          'onkeyup': "javascript:yesnoCheck()"}))
    cexpyear = forms.CharField(max_length=4, label='Expiry Year :',
                               widget=forms.TextInput
                               (attrs={'type': 'number', 'max': '2050', 'min': '2021', 'class': 'form-control',
                                       'style': 'width:500px', 'onkeyup': "javascript:yesnoCheck()"}))
    cexpmonth = forms.CharField(max_length=2, label='Expiry Month :',
                                widget=forms.TextInput
                                (attrs={'type': 'number', 'max': '13', 'min': '01', 'class': 'form-control',
                                        'style': 'width:500px', 'onkeyup': "javascript:yesnoCheck()"}))
    cnameoncard = forms.CharField(max_length=100, label='Name on Card:',
                                  widget=forms.TextInput
                                  (attrs={'class': 'form-control', 'style': 'width:500px',
                                          'onkeyup': "javascript:yesnoCheck()"}))
    ccvv = forms.CharField(max_length=3, label='CVV :',
                           widget=forms.TextInput
                           (attrs={'type': 'number', 'class': 'form-control', 'style': 'width:500px',
                                   'onkeyup': "javascript:yesnoCheck()"}))

    class Meta:
        model = User3Profile
        fields = ('ccardnumber', 'cexpyear', 'cexpmonth', 'cnameoncard', 'ccvv')


class AddUpiid(forms.ModelForm):
    upiid = forms.CharField(max_length=100, label='UPI ID :',
                            widget=forms.TextInput
                            (attrs={'class': 'form-control', 'style': 'width:500px',
                                    'onkeyup': "javascript:yesnoCheck2()"}))

    class Meta:
        model = User5Profile
        fields = ('upiid',)


class AddPaytmno(forms.ModelForm):
    paytmnumber = forms.CharField(max_length=10, label='Paytm linked Number :',
                                  widget=forms.TextInput
                                  (attrs={'type': 'number', 'class': 'form-control', 'style': 'width:500px',
                                          'onkeyup': "javascript:yesnoCheck()"}))

    class Meta:
        model = User6Profile
        fields = ('paytmnumber',)


class PhoneForm(forms.ModelForm):
    phone = forms.IntegerField(label='Phone :',
                               widget=forms.TextInput
                               (attrs={'type': 'number', 'class': 'form-control', 'style': 'width:500px',
                                       'onkeyup': "javascript:yesnoCheck1()"}))

    class Meta:
        model = User2Profile
        fields = ('phone',)


class AddressForm(forms.ModelForm):
    address = forms.CharField(max_length=100, label='Address :',
                              widget=forms.TextInput
                              (attrs={'class': 'form-control', 'style': 'width:500px',
                                      'onkeyup': "javascript:yesnoCheck()"}))
    city = forms.CharField(max_length=100, label='City :',
                           widget=forms.TextInput
                           (attrs={'class': 'form-control', 'style': 'width:500px',
                                   'onkeyup': "javascript:yesnoCheck()"}))
    state = forms.CharField(max_length=100, label='State :',
                            widget=forms.TextInput
                            (attrs={'class': 'form-control', 'style': 'width:500px',
                                    'onkeyup': "javascript:yesnoCheck()"}))
    pin_code = forms.IntegerField(label='Pin Code :',
                                  widget=forms.TextInput
                                  (attrs={'class': 'form-control', 'style': 'width:500px',
                                          'onkeyup': "javascript:yesnoCheck()"}))
    country = forms.CharField(max_length=100, label='Country :',
                              widget=forms.TextInput
                              (attrs={'class': 'form-control', 'style': 'width:500px',
                                      'onkeyup': "javascript:yesnoCheck()"}))

    class Meta:
        model = User1Profile
        fields = ('address', 'city', 'state', 'pin_code', 'country')
