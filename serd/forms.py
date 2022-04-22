from datetime import datetime
from urllib import request
from dal import autocomplete
from django import forms
from slugify import slugify
from django.core.exceptions import ValidationError
from serd.choices import CURRENT_ACCOMODATION, LANGUAGE_CHOICE, OFFER_STATE, PETS, PRIORITY_CHOICE, REQUEST_STATE
from .models import HousingRequest, Offer
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from .mail import Mailer
from django.contrib.admin.widgets import FilteredSelectMultiple

def isascii(s):
    """Check if the characters in string s are in ASCII, U+0-U+7F."""
    return len(s) == len(s.encode())

PFLICHT = ValidationError(_("Pflichtfeld"))
class OfferForm(forms.ModelForm):
    def test_required(self, field:str):
        data = self.cleaned_data[field]
        if data is None or data == "":
            self.add_error(field=field, error=PFLICHT)
        return data

    template_name = 'serd/form_snippet.html'
    available_from =  forms.DateField(
        label=_('Verfügbar ab'),
        widget=forms.SelectDateWidget(years=range(2022, 2024))) 
    available_until =  forms.DateField(
        label=_('Verfügbar bis'), required=False,
        widget=forms.SelectDateWidget(years=range(2022, 2024))) 
    cost = forms.IntegerField(label=_("falls verlangt, Monatsmiete warm"), required=False)
    comment = forms.CharField(required=False, label=_("Weiterer Kommentar (max. 250 Zeichen)"), widget=forms.Textarea)

    def clean_last_name(self):
        return self.test_required('last_name')

    def clean_given_name(self):
        return self.test_required('given_name')
    
    def clean_plz(self):
        return self.test_required('plz')

    def clean_total_number(self):
        return self.test_required('total_number')
    
    def clean_children_number(self):
        return self.test_required('children_number')

    def clean_city(self):
        return self.test_required('city')
    def clean_mail(self):
        return self.test_required('mail')
    
    def clean_rooms(self):
        return self.test_required('rooms')

    def clean(self):
        if self.errors:
            return self.cleaned_data
        if not self.cleaned_data.get('total_number') > self.cleaned_data.get('children_number'):
            self.add_error(field='total_number', error=
            ValueError(
                _("Mindestens eine erwachsene Person")
                ))
        if self.cleaned_data.get('limited_availability'):
            available_from = self.cleaned_data.get('available_from')
            available_until = self.cleaned_data.get('available_until')
            if (available_until <= available_from):
                self.add_error(field='available_until', error=
                ValueError(
                    _("Ende der Verfügbarkeit muss später als der Beginn sein")
                ))
        if not self.cleaned_data.get('seperate_appartment') and not self.cleaned_data.get('living_with'):
            self.add_error(field='living_with', error=
            ValueError(
                _("Eigene Wohnsituation muss angegeben werden, wenn die Unterbringung nicht in einer getrennten Wohnung erfolgt")
            ))
        if not self.cleaned_data.get('for_free') and not self.cleaned_data.get('cost'):
            self.add_error(field='for_free', error=
            ValueError(
                _("Bitte bestätigen Sie, dass die Unterkunft kostenfrei überlassen wird, oder geben Sie die Miethöhe an")
            ))
        if self.cleaned_data.get('for_free') and self.cleaned_data.get('cost'):
            self.add_error(field='cost', error=
                ValueError(
                _("Bei kostenfreier Unterkunft ist keine Mietangabe möglich")
            ))
        return self.cleaned_data

    def save(self, commit=True, **kwargs):
        offer = super(OfferForm, self).save(commit=False, **kwargs)
        if commit:
             offer.save()
        if not isinstance(self, OfferEditForm):
            mailer = Mailer()
            mailer.send_offer_confirmation_mail(offer)
        return offer

        
    class Meta :
        model = Offer
        fields =('given_name', 'last_name',  'plz','city', 'street', 'phone', 'mail',
        'language', 'additional_languages', 'total_number' , 'children_number' , 'for_free' , 'cost', 'spontan', 
        'available_from', 'limited_availability', 'available_until','accessability', 'public_transport', 
        'rooms', 'seperate_appartment', 'living_with', 'pets', 'covid', 'comment')
    
class OfferEditForm(OfferForm):
    private_comment = forms.CharField(required=False, label=_("Interner Kommentar"), widget=forms.Textarea)
    number = forms.IntegerField(label="Laufende Nr.", disabled=True, required=False)
    class Meta:
        model = Offer
        fields = OfferForm.Meta.fields + ('number', 'by_municipality', 'private_comment', 'state')

class RequestForm(forms.ModelForm):
    template_name = 'form_snippet.html'
    def test_required(self, field:str):
        data = self.cleaned_data[field]
        if data is None or data == "":
            self.add_error(field=field, error=PFLICHT)
        return data

    arrival_date = forms.DateTimeField(label=_('Ankunftstag'),
        widget=forms.SelectDateWidget(years=range(2022, 2024))
    )
    who = forms.CharField(label=_("Bitte beschreiben Sie Ihre Gruppe kurz (Alter, Geschlecht, ...)"), required=False, widget=forms.Textarea)

    class Meta:
        model = HousingRequest
        fields =('given_name', 'last_name', 'phone', 'mail', 'adults', 'children', 'who',
        'split', 'current_housing', 'can_pay', 'representative', 'repr_mail', 'repr_phone', 'arrival_date', 
        'arrival_location', 'pets', 'pet_number', 'car', 'languages', 'additional_languages', 'vaccination', 'accessability_needs')
    def clean_given_name(self):
        return self.test_required('given_name')
    def clean_last_name(self):
        return self.test_required('last_name')
    def clean_phone(self):
        return self.test_required('phone')
    def clean_mail(self):
        return self.test_required('mail')
    def clean_adults(self):
        return self.test_required('adults')
    def clean_children(self):
        return self.test_required('children')
    def clean_who(self):
        return self.test_required('who')
    def clean_arrival_location(self):
        return self.test_required('arrival_location')
    def clean_arrival_date(self):
        date = self.cleaned_data['arrival_date']
        if date.date() == datetime.strptime("01.01.22","%d.%m.%y").date():
            self.add_error(field='arrival_date', error=PFLICHT)
        return date
    def clean_current_housing(self):
        return self.test_required('current_housing')

    def clean(self):
        pets = self.cleaned_data.get('pets')
        if pets and len(pets) > 1 and 'none' in pets:
            self.add_error(field='pets', error=ValueError(
                _("Ungültige Auswahl: 'Keine' schließt die anderen Wahlmöglichkeiten aus.")
            ))
        if pets == ['none']:
            if self.cleaned_data.get('pet_number'):
                self.add_error(field='pet_number', error=ValueError(
                    _("Auswahl 'Keine' bei Haustier widerspricht Anzahl 0")
                ))
            else:
                self.cleaned_data['pet_number'] = 0
        elif not self.cleaned_data.get('pet_number'):
            self.add_error(field='pets', error=ValueError(
                    _("Wenn keine Haustiere vorhanden sind, muss 'Keine' ausgewählt werden.")
                ))
        
        elif pets and 'none' not in pets and len(pets) > self.cleaned_data.get('pet_number'):
            self.add_error(field='pet_number', error=ValueError(
                    _("Mehr Tierarten ausgewählt als Tiere vorhanden")
                ))
        return self.cleaned_data

    def save(self, commit=True, **kwargs):
        """Slugify the name if it is not in ASCII to make live easier for case handlers who
        can't read cyrillic 
        """
        housingrequest = super(RequestForm, self).save(commit=False, **kwargs)
        if not isascii(housingrequest.given_name) or not isascii(housingrequest.last_name):
            housingrequest.name_slug  = slugify(housingrequest.given_name)+" "+ slugify(housingrequest.last_name)
        
        if commit:
            housingrequest.save()
        if not isinstance(self, RequestEditForm):
            mailer = Mailer()
            mailer.send_request_confirmation_mail(housingrequest)
        return housingrequest


class RequestEditForm(RequestForm):
    private_comment = forms.CharField(label=_("Interner Kommentar"), required=False, widget=forms.Textarea)
    number = forms.IntegerField(label="Laufende Nr.", disabled=True, required=False)
    # override here with do nothing clean method to allow empty arrival location when editing
    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['case_handler'].queryset = User.objects.order_by('username')
    def clean_arrival_location(self):
        data = self.cleaned_data['arrival_location']
        return data
    
    def save(self, commit=True):
        request = super(RequestEditForm, self).save(commit=False)
        hosts = self.cleaned_data['possible_hosts']
        if hosts:
            request.possible_hosts.add(*hosts)
        if commit:
            request.save()
        return request

    class Meta:
        model = HousingRequest
        fields = RequestForm.Meta.fields + ('number', 'state','case_handler', 'placed_at', 'hotel', 'priority','private_comment', 'possible_hosts')
        widgets= {'possible_hosts': autocomplete.ModelSelect2Multiple(url='offer-autocomplete')}

BOOL_CHOICES = (('null', 'Egal'), ('True','Ja'),('False', 'Nein'))
class RequestFilterForm(forms.Form):
    num_min = forms.IntegerField(min_value=0,required=False, label="Personen von")
    num_max = forms.IntegerField(min_value=0, required=False, label="Personen bis")
    split = forms.ChoiceField(choices=BOOL_CHOICES, label="Teilbar")
    current_housing = forms.MultipleChoiceField(choices=CURRENT_ACCOMODATION, label="Aktuelle Unterbringung", required=False, widget=forms.CheckboxSelectMultiple)
    pets = forms.MultipleChoiceField(choices=PETS, required=False, widget=forms.CheckboxSelectMultiple, label="Haustiere")
    languages = forms.MultipleChoiceField(choices=LANGUAGE_CHOICE, required=False, widget=forms.CheckboxSelectMultiple, label="Sprachen")
    accessability_needs = forms.ChoiceField(choices=BOOL_CHOICES, label="Barrierefrei")
    priority = forms.MultipleChoiceField(choices=PRIORITY_CHOICE, required=False, label="Priorität", widget=forms.CheckboxSelectMultiple)
    state = forms.MultipleChoiceField(choices=REQUEST_STATE, required=False, label="Status", widget=forms.CheckboxSelectMultiple)
    no_handler = forms.BooleanField(label="Kein Sachbearbeiter", required=False)
    case_handler = forms.ModelChoiceField(queryset=User.objects.order_by('username'), required=False)

class OfferFilterForm(forms.Form):
    num_min = forms.IntegerField(min_value=0,required=False, label="Personen von")
    num_max = forms.IntegerField(min_value=0, required=False, label="Personen bis")
    PLZ = forms.CharField(max_length=5, required=False, label='PLZ')
    city = forms.CharField(max_length=128, required=False, label='Ort')
    cost_min = forms.IntegerField(min_value=0, required=False, label='Kosten von')
    cost_max = forms.IntegerField(min_value=0, required=False, label='Kosten bis')
    language = forms.MultipleChoiceField(choices=LANGUAGE_CHOICE, required=False, label="Sprachen", widget=forms.CheckboxSelectMultiple)
    spontan = forms.ChoiceField(choices=BOOL_CHOICES, label='Spontan')
    limited = forms.ChoiceField(choices=BOOL_CHOICES, label='Begrenzt verfügbar')
    appartment = forms.ChoiceField(choices=BOOL_CHOICES, label='Eigene Wohnung')
    pets = forms.MultipleChoiceField(choices=PETS, required=False, label='Haustiere', widget=forms.CheckboxSelectMultiple)
    accessability = forms.ChoiceField(choices=BOOL_CHOICES, label="Barrierefrei")
    state = forms.MultipleChoiceField(choices=OFFER_STATE, label='Status', widget=forms.CheckboxSelectMultiple, required=False)
    for_free = forms.ChoiceField(choices=BOOL_CHOICES, label='Gratis')