from django import forms
from .models import HousingRequest, Offer


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
        fields =('given_name', 'last_name',  'plz','city','street', 'phone', 'mail',
        'language', 'cost', 'spontan', 'available_from', 'limited_availability', 'available_until',
        'accessability', 'public_transport', 'rooms', 'seperate_appartment', 'living_with', 'pets', 'comment')
    
class OfferEditForm(OfferForm):
    class Meta:
        model = Offer
        fields = OfferForm.Meta.fields + ('private_comment', 'state')

class RequestForm(forms.ModelForm):
    arrival_date = forms.DateTimeField(
        widget=forms.SelectDateWidget(years=range(2022, 2024))
    )
    class Meta:
        model = HousingRequest
        fields =('given_name', 'last_name', 'phone', 'mail', 'adults', 'children', 'who',
        'split', 'current_housing', 'arrival_date', 'arrival_location', 'pets', 'pet_number',
        'car', 'languages', 'vaccination', 'accessability_needs')

class RequestEditForm(RequestForm):
    class Meta:
        model = HousingRequest
        fields = RequestForm.Meta.fields + ('state','case_handler','placed_at', 'priority','private_comment')