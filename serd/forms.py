from dal import autocomplete    
from django import forms
from slugify import slugify
from datetime import date
from django.core.exceptions import ValidationError
from serd.choices import CURRENT_ACCOMODATION, LANGUAGE_CHOICE, OFFER_SORT, OFFER_STATE, PETS, PRIORITY_CHOICE, REQUEST_SORT, REQUEST_STATE, SORT_DIRECTION
from .models import Hotel, HousingRequest, Offer, OfferFilter, Profile, HotelStay, RequestFilter
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from django.forms import modelformset_factory, BaseModelFormSet
from .mail import Mailer
from .utils.date import overlaps



def isascii(s):
    """Check if the characters in string s are in ASCII, U+0-U+7F."""
    return len(s) == len(s.encode())

PFLICHT = ValidationError(_("Pflichtfeld"))
class OfferForm(forms.ModelForm):
    def test_required(self, field:str):
        data = self.cleaned_data[field]
        if data is None or data == "" or data == []:
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
    comment = forms.CharField(required=False, label=_("Weiterer Kommentar (max. 500 Zeichen)"), widget=forms.Textarea)

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
    
    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if len(comment) > 500:
            self.add_error(field='comment', error=ValidationError(_("Maximal 500 Zeichen (aktuell: {})").format(len(comment))))
        return comment
    
    def clean_language(self):
        
        return self.test_required('language')


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
    def clean_language(self):
        return self.cleaned_data['language']
    def clean_comment(self):
        return self.cleaned_data['comment']
    class Meta:
        model = Offer
        fields = OfferForm.Meta.fields + ('number', 'by_municipality', 'private_comment', 'state')

class RequestForm(forms.ModelForm):
    template_name = 'form_snippet.html'
    def test_required(self, field:str):
        data = self.cleaned_data[field]
        if not settings.DEBUG and (data is None or data == ""):
            self.add_error(field=field, error=PFLICHT)
        return data

    arrival_date = forms.DateField(label=_('Ankunftstag'), required=False, widget=forms.SelectDateWidget(years=range(2022, 2024)))
    who = forms.CharField(label=_("Bitte beschreiben Sie Ihre Gruppe kurz (Alter, Geschlecht, ...)"), required=False, widget=forms.Textarea)

    class Meta:
        model = HousingRequest
        fields =('given_name', 'last_name', 'phone', 'mail', 'adults', 'children', 'who',
        'split', 'current_housing', 'can_pay', 'representative', 'repr_mail', 'repr_phone', 'arrival_date', 
        'pets', 'pet_number', 'car', 'languages', 'additional_languages', 'vaccination', 'smoker', 'accessability_needs', 'profession')
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
    def clean_arrival_date(self):
             return self.test_required('arrival_date')
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
                    _("Auswahl 'Keine' bei Haustier widerspricht Anzahl ungleich 0")
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

    
    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['case_handler'].queryset = User.objects.order_by('username')

    def save(self, commit=True):
        request = super(RequestEditForm, self).save(commit=False)
        hosts = self.cleaned_data['possible_hosts']
        if request.number:
            request.possible_hosts.remove(*request.possible_hosts.difference(hosts))
            request.possible_hosts.add(*hosts)
        if commit:
            request.save()
        return request

    class Meta:
        model = HousingRequest
        fields = RequestForm.Meta.fields + ('number', 'state','case_handler', 'placed_at', 'possible_hosts', 'private_comment')
        widgets= {'possible_hosts': autocomplete.ModelSelect2Multiple(url='offer-autocomplete')}

class RequestFormForHotels(RequestForm):
    private_comment = forms.CharField(label=_("Interner Kommentar"), required=False, widget=forms.Textarea)
    class Meta:
        fields = RequestForm.Meta.fields + ('number', 'state',  'private_comment')
        model = HousingRequest

class HotelStayForm(forms.ModelForm):
    arrival_date = forms.DateField(required= False, label="Anreisetag", widget=forms.SelectDateWidget(years=range(2022, 2024)))
    departure_date = forms.DateField(required= False, label="Abreisetag", widget=forms.SelectDateWidget(years=range(2022, 2024)))
    hotel= forms.ModelChoiceField(required = False, label="Hotel", queryset=Hotel.objects.all())
    room = forms.CharField(required=False, label="Zimmer", max_length=64)
    def clean_arrival_date(self):
        return self.test_required('arrival_date')
    
    def clean_hotel(self):
        return self.test_required('hotel')

    def clean(self):
        arrival = self.cleaned_data.get('arrival_date')
        departure = self.cleaned_data.get('departure_date')
        if departure:
            if departure <= arrival:
                self.add_error(field='departure_date', error=ValidationError("Abreise muss nach der Ankunft sein"))

        return self.cleaned_data
    def test_required(self, field:str):
        data = self.cleaned_data[field]
        if data is None or data == "":
            self.add_error(field=field, error=PFLICHT)
        return data
    class Meta:
        model = HotelStay
        fields = ('arrival_date', 'departure_date', 'room', 'hotel')

class BaseStaySet(BaseModelFormSet):
    def clean(self):
        if any(self.errors):
            return
        intervals = []
        form: HotelStayForm
        for form in self.forms:
            arrival = form.cleaned_data.get('arrival_date')
            if not arrival:
                continue
            departure = form.cleaned_data.get('departure_date')
            if not departure:
                departure = date.max
            if any(overlaps((arrival, departure), interval) for interval in intervals):
                form.add_error('arrival_date', ValidationError("Ankunft darf nicht vor vorhergehender Abreise liegen"))
            intervals.append((arrival, departure))

StaySet = modelformset_factory(HotelStay, HotelStayForm, formset=BaseStaySet)

BOOL_CHOICES = (('null', 'Egal'), ('True','Ja'),('False', 'Nein'))


class OfferFilterForm(forms.ModelForm):
    class Meta:
        exclude = []
        model = OfferFilter
    
class RequestFilterForm(forms.ModelForm):
    class Meta:
        exclude = []
        model = RequestFilter

class ProfileForm(forms.ModelForm):
    
    languages = forms.MultipleChoiceField(choices=LANGUAGE_CHOICE, required=False, label="Sprachen", widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Profile
        fields=('name', 'phone', 'whatsapp', 'signal','threema' ,'telegram', 'mail', 'languages', 'comment')


class InvoiceSelectionForm(forms.Form):
    
    start = forms.DateField(label='von', widget=forms.SelectDateWidget(years=range(2022, 2024)))
    end = forms.DateField(label='bis', widget=forms.SelectDateWidget(years=range(2022, 2024)))
    def clean(self):
        if self.cleaned_data['end'] <= self.cleaned_data['start']:
            self.add_error(field='start', error=ValidationError("Ungültiger Zeitraum"))


