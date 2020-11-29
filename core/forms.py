from django import forms
from registration.forms import RegistrationFormUniqueEmail
from django.utils.translation import gettext_lazy as _


class CommercialForm(forms.Form):
    title = forms.CharField(help_text=_('Title'), max_length=300, required=True, widget=forms.TextInput
                            (attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(help_text=_('Quantity'),widget=forms.TextInput
                            (attrs={'class': 'form-control'}))
    price = forms.IntegerField(help_text=_('Price'),widget=forms.TextInput
                            (attrs={'class': 'form-control'}))
    details = forms.CharField(help_text=_('Details'),widget=forms.Textarea
                            (attrs={'class': 'form-control'}))
    file = forms.FileField(help_text=_('File Details'),widget=forms.TextInput
                            (attrs={'class': 'form-control'}))


class ProfileForm(RegistrationFormUniqueEmail):
    full_name = forms.CharField(help_text=_('Full Name'), max_length=300, required=True, widget=forms.TextInput
                            (attrs={'class': 'form-control'}))
    phone_number = forms.CharField(help_text=_('Phone Number'),widget=forms.TextInput
                            (attrs={'class': 'form-control'}))
    address_1 = forms.CharField(help_text=_('Address 1'),max_length=300,required=True,widget= forms.TextInput
                            (attrs={'class':'form-control'}))
    address_2 = forms.CharField(help_text=_('Address 2'), max_length=300, required=True, widget=forms.TextInput
                            (attrs={'class': 'form-control'}))
    country = forms.CharField(max_length=300, required=True,widget= forms.TextInput
                            (attrs={'class':'form-control'}),help_text=_("Country"))
    state = forms.CharField(max_length=300, help_text=_("State"),required=True,widget= forms.TextInput
                            (attrs={'class':'form-control'}))
    ZIP = forms.CharField(max_length=300, help_text=_("ZIP"),required=True,widget= forms.TextInput
                            (attrs={'class':'form-control'}))

