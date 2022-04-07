from django import forms
from .models import HousingRequest, Offer
from django.utils.translation import gettext_lazy as _

class OfferForm(forms.ModelForm):
    available_from =  forms.DateField(
        widget=forms.SelectDateWidget(years=range(2022, 2024))) 
    available_until =  forms.DateField(
        widget=forms.SelectDateWidget(years=range(2022, 2024))) 
    def clean(self):
        if self.cleaned_data['limited_availability']:
            available_from = self.cleaned_data['available_from']
            available_until = self.cleaned_data['available_until']
            if (available_until <= available_from):
                self.add_error(field='available_until', error=
                ValueError(
                    _("Ende der Verfügbarkeit muss später als der Beginn sein")
                ))

        return self.cleaned_data
        
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
    pet_number = forms.IntegerField(required=False)
    class Meta:
        model = HousingRequest
        fields =('given_name', 'last_name', 'phone', 'mail', 'adults', 'children', 'who',
        'split', 'current_housing', 'arrival_date', 'arrival_location', 'pets', 'pet_number',
        'car', 'languages', 'vaccination', 'accessability_needs')
    def clean(self):
        pets = self.cleaned_data['pets']
        if len(pets) > 1 and 'none' in pets:
            self.add_error(field='pets', error=ValueError(
                _("Ungültige Auswahl: 'Keine' schließt die anderen Wahlmöglichkeiten aus.")
            ))
        if pets == ['none']:
            if self.cleaned_data['pet_number']:
                self.add_error(field='pet_number', error=ValueError(
                    _("Auswahl 'Keine' bei Haustier widerspricht Anzahl ≠ 0")
                ))
            else: self.cleaned_data['pet_number'] = 0
        elif not self.cleaned_data['pet_number']:
            self.add_error(field='pets', error=ValueError(
                    _("Wenn keine Haustiere vorhanden sind, muss 'Keine' ausgewählt werden.")
                ))
        if 'none' not in pets and len(pets) > self.cleaned_data['pet_number']:
            self.add_error(field='pet_number', error=ValueError(
                    _("Mehr Tierarten ausgewählt als Tiere vorhanden")
                ))
        return self.cleaned_data

class RequestEditForm(RequestForm):
    class Meta:
        model = HousingRequest
        fields = RequestForm.Meta.fields + ('state','case_handler','placed_at', 'priority','private_comment')