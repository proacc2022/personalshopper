from django import forms

from user.models import *


class OrderForm(forms.Form):
    addoptionselection = forms.ModelChoiceField(queryset=User1Profile.objects.all(), empty_label=None,
                                                to_field_name="id")
    phoneoptionselection = forms.ModelChoiceField(queryset=User2Profile.objects.all(), empty_label=None,
                                                  to_field_name="id")
    CHOICES = [('Express Delivery', 'Express Delivery'),
               ('Regular Delivery(FREE)', 'Regular Delivery(FREE)')]
    deloptionselection = forms.ChoiceField(choices=CHOICES,
                                           widget=forms.RadioSelect(attrs={'onclick': 'dislaydeliverycharge()'}))
    paymethodselection = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        # self.tyy = (kwargs.pop('tyy', None))
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['addoptionselection'].label_from_instance = self.label_from_instance
        self.fields['phoneoptionselection'].label_from_instance = self.label_from_instance2
        self.fields['addoptionselection'].label = "Address"
        self.fields['phoneoptionselection'].label = "Contact"
        self.fields['paymethodselection'].label = "Payment Method"
        self.fields['deloptionselection'].label = "Delivery Option"
        # self.fields['addoptionselection'].queryset = User1Profile.objects.filter(id=self.tyy)

    @staticmethod
    def label_from_instance(obj):
        print(obj.address + '' + obj.city + '' + obj.state + '' + obj.pin_code + '' + obj.country)
        return obj.address + '' + obj.city + '' + obj.state + '' + obj.pin_code + '' + obj.country

    @staticmethod
    def label_from_instance2(obj):
        print(obj.phone)
        return obj.phone

    # def fulladdress(self):
    #     adddata = User1Profile.objects.all().filter(id=User.id)
    #     for x in adddata:
    #
    #     return self.user.address + ' ' + self.user.city + self.user.state + ' ' + self.user.pin_code
    #     + ' ' + self.user.country
    #
    # class Meta:
    #     model = User1Profile
    #     fields = ['adress_joined','payment_method']


class addcreditcard(forms.ModelForm):
    ccardnumber = forms.CharField(max_length=16, label='Card Number :',
                              widget=forms.TextInput
                              (attrs={'type':'number', 'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))
    cexpyear = forms.CharField(max_length=4, label='Expiry Year :',
                           widget=forms.TextInput
                           (attrs={'type':'number', 'max':'2050', 'min':'2021', 'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))
    cexpmonth = forms.CharField(max_length=2, label='Expiry Month :',
                            widget=forms.TextInput
                            (attrs={'type':'number', 'max':'13', 'min':'01', 'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))
    cnameoncard = forms.CharField(max_length=100, label='Name on Card:',
                                  widget=forms.TextInput
                                  (attrs={'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))
    ccvv = forms.CharField(max_length=3, label='CVV :',
                              widget=forms.TextInput
                              (attrs={'type':'number', 'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))

    class Meta:
        model = User3Profile
        fields = ('ccardnumber', 'cexpyear', 'cexpmonth', 'cnameoncard', 'ccvv')

class adddebitcard(forms.ModelForm):
    dcardnumber = forms.CharField(max_length=16, label='Card Number :',
                              widget=forms.TextInput
                              (attrs={'type':'number', 'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))
    dexpyear = forms.CharField(max_length=4, label='Expiry Year :',
                           widget=forms.TextInput
                           (attrs={'type':'number', 'max':'2050', 'min':'2021', 'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))
    dexpmonth = forms.CharField(max_length=2, label='Expiry Month :',
                            widget=forms.TextInput
                            (attrs={'type':'number', 'max':'13', 'min':'01', 'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))
    dnameoncard = forms.CharField(max_length=100, label='Name on Card:',
                                  widget=forms.TextInput
                                  (attrs={'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))
    dcvv = forms.CharField(max_length=3, label='CVV :',
                              widget=forms.TextInput
                              (attrs={'type':'number', 'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))

    class Meta:
        model = User4Profile
        fields = ('dcardnumber', 'dexpyear', 'dexpmonth', 'dnameoncard', 'dcvv')

class addupiid(forms.ModelForm):
    upiid = forms.CharField(max_length=100, label='UPI ID :',
                              widget=forms.TextInput
                              (attrs={'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))

    class Meta:
        model = User5Profile
        fields = ('upiid',)

class addpaytmno(forms.ModelForm):
    paytmnumber = forms.CharField(max_length=10, label='Paytm linked Number :',
                              widget=forms.TextInput
                              (attrs={'type':'number', 'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))

    class Meta:
        model = User6Profile
        fields = ('paytmnumber',)

class phoneform(forms.ModelForm):
    phone = forms.IntegerField(label='Phone :',
                               widget=forms.TextInput
                               (attrs={'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))

    class Meta:
        model = User2Profile
        fields = ('phone',)

class addressform(forms.ModelForm):
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
                                  (attrs={'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))
    country = forms.CharField(max_length=100, label='Country :',
                              widget=forms.TextInput
                              (attrs={'class': 'form-control', 'style': 'width:500px', 'required': 'true'}))

    class Meta:
        model = User1Profile
        fields = ('address', 'city', 'state', 'pin_code', 'country')