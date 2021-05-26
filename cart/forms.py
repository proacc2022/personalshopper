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
