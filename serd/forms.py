import imp
from django import forms
from .models import Offer


class OfferForm(forms.ModelForm):
    available_from =  forms.DateField(
        widget=forms.SelectDateWidget(years=range(2022, 2024))) 
    available_until =  forms.DateField(
        widget=forms.SelectDateWidget(years=range(2022, 2024))) 
    def clean_available_from (self):
        available_from = self.cleaned_data['available_from']
        print(available_from)
        return available_from
    class Meta :
        model = Offer
        fields =('given_name', 'last_name',  'plz', 'phone', 'mail',
        'language', 'cost', 'spontan', 'available_from', 'limited_availability', 'available_until',
        'accessability', 'public_transport', 'rooms', 'seperate_appartment', 'living_with', 'pets', 'comment')
    
class OfferEditForm(OfferForm):
    class Meta:
        model = Offer
        fields = OfferForm.Meta.fields + ('private_comment', 'state')
        