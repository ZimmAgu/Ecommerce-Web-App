from random import choices
from django import forms
from django_countries.fields import CountryField

PAYMENT_CHOICES = (
    ('st', 'Stripe'),
    ('pp', 'Paypal')
)

class checkoutForm(forms.Form):
    streetAddress = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '1234 Main St'}))
    apartmentAddress = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Apartment or suite'}))
    country = CountryField(blank_label='(select country)').formfield()
    zipCode = forms.CharField()
    paymentChoice = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)
