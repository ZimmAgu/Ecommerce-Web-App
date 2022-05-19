from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from . import formChoices

class checkoutForm(forms.Form):
    streetAddress = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '1234 Main St', 'size': 50}))
    apartmentAddress = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Apartment or suite', 'size': 50}))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={'class' : 'custom-select d-block w-100'}))
    state = forms.ChoiceField(widget=forms.Select(attrs={'class' : 'form-control'}), choices=formChoices.STATE_CHOICES)
    zipCode = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    paymentChoice = forms.ChoiceField(widget=forms.RadioSelect(), choices=formChoices.PAYMENT_CHOICES)
