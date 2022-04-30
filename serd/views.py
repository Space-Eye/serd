from django.urls import reverse

from serd.choices import PETS
from .models import Hotel, HotelStay, HousingRequest, Offer, NewsItem, Profile
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView, FormView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
from .forms import OfferEditForm, OfferForm, RequestEditForm, RequestFilterForm, RequestForm, OfferFilterForm, ProfileForm, InvoiceSelectionForm, HotelStayForm
from dal import autocomplete
from django.db.models import Sum
from django.forms import modelformset_factory


class OfferAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        print("callled")
        if not self.request.user.is_authenticated:
            return Offer.objects.none()
        qs = Offer.objects.all()
        if self.q:
            try:
                qs = qs.filter(number=int(self.q))
            except:
                qs =qs.filter(last_name__istartswith=self.q)
        return qs

def success(request):
    return HttpResponse("success")

@login_required
def index(request):
    context = {'dataset': NewsItem.objects.all()}
    return render(request, "serd/index.html", context)


class AddRequest(CreateView):
    model = HousingRequest
    form_class = RequestForm
    def get_success_url(self) -> str:
        return reverse('success_request', args=(self.object.number,))

StaySet = modelformset_factory(HotelStay, HotelStayForm)

@login_required
def internal_add_housingrequest(request):
        if request.method =='GET':
            requestform = RequestEditForm(prefix='request')
            stayset = StaySet(prefix='stays')
        
            return render(request, 'serd/request_form_intern.html', {'stayset': stayset, 'requestform': requestform} )
        elif request.method == 'POST':
            requestform = RequestEditForm(request.POST, prefix='request')
            stayset = StaySet(request.POST, prefix='stays')
            if stayset.is_valid() and requestform.is_valid():
                req = requestform.save()
            for stayform in stayset:
                stay = stayform.save(commit=False)
                stay.request = req
                stay.save()            
                return HttpResponseRedirect(reverse('index'))
            return render(request, 'serd/request_form_intern.html', {'stayset': stayset, 'requestform': requestform})
            



class AddOffer(CreateView):
    model = Offer
    form_class = OfferForm
    
    def get_success_url(self) -> str:

        return reverse('success_offer', args=(self.object.number,))

class InternalAddOffer(CreateView):
    model = Offer
    form_class = OfferEditForm
    def get_success_url(self) -> str:
        return reverse('index')

@login_required
def request_list(request):

    context = {}
    context["dataset"] = HousingRequest.objects.all()
    return render(request, "serd/request_list.html", context)

@login_required
def offer_list(request):
    context = {}
    context["dataset"] = Offer.objects.all()
    return render(request, "serd/offer_list.html", context)
   


@login_required
def hotel_list(request):
    hotels =  list(Hotel.objects.all())

    for hotel in hotels:
        stays = HotelStay.objects.filter(hotel=hotel, arrival_date__lte=date.today())
        stays = stays.filter(Q(departure_date__gte=date.today())| Q(departure_date__isnull=True))
        adults = stays.aggregate(Sum('request__adults'))['request__adults__sum']
        if not adults:
            adults = 0 # Can't do math with none
        children =  stays.aggregate(Sum('request__children'))['request__children__sum']
        if not children:
            children = 0 # Can't do math with none
        hotel.beds_free = hotel.beds -adults - children
        hotel.requests = HousingRequest.objects.filter(stays__in =stays)
    context = {}
    context["dataset"] = hotels
    
    return render(request, "serd/hotel_list.html", context)

class OfferUpdate(UpdateView):
    success_url = "/offers"
    def get_object(self, queryset=None):
        return Offer.objects.get(number=self.kwargs["offer_id"])
    form_class = OfferEditForm


@login_required
def request_update(request, request_id):
        if request.method =='GET':
            housingreq = HousingRequest.objects.get(number = int(request_id))
            stays = HotelStay.objects.filter(request = housingreq)
            requestform = RequestEditForm(instance=housingreq, prefix="request")
            stayset = StaySet(queryset=stays, prefix='stays')
            return render(request, 'serd/request_form_intern.html', {'requestform': requestform, 'stayset': stayset} )
        elif request.method == 'POST':
            housingreq = housingreq = HousingRequest.objects.get(number = int(request_id))
            requestform = RequestEditForm(request.POST, instance=housingreq, prefix='request')
            stays = HotelStay.objects.filter(request = housingreq)
            stayset = StaySet(request.POST, queryset=stays, prefix='stays')
            if stayset.is_valid() and requestform.is_valid():
                request = requestform.save()
                stays =stayset.save(commit=False)
                for stay in stays:
                    try:
                        stay.request
                    except HousingRequest.DoesNotExist:
                        stay.request = housingreq
                    stay.save()
                return HttpResponseRedirect(reverse('index'))
            
            return render(request, 'serd/request_form_intern.html', {'requestform': requestform, 'stayset': stayset} )
        
class SuccessOffer(TemplateView):
    template_name = "serd/success_offer.html"
  

class SuccessRequest(TemplateView):
    template_name = "serd/success_request.html"
  
class RequestFilter(FormView):
    template_name = "serd/request_filter.html"
    form_class = RequestFilterForm

    def form_valid(self, form) -> HttpResponse:
        queryset = HousingRequest.objects.all()
        num_min = form.cleaned_data['num_min']
        if num_min:
            queryset = queryset.filter(persons__gte=num_min)
        num_max = form.cleaned_data['num_max']
        if num_max:
            queryset = queryset.filter(persons__lte=num_max)
        split = form.cleaned_data['split']
        if split != 'null':
            queryset = queryset.filter(split__exact=split)
        housing = form.cleaned_data['current_housing']
        if housing:
            q = Q()
            for acc in housing:
                q = q |Q(current_housing__exact=acc)
            queryset = queryset.filter(q)
        pets = form.cleaned_data['pets']
        if pets:
            q = Q()
            for choice in PETS:
                if choice[0] in pets:
                    q = q & Q(pets__contains=choice[0])
                else:
                    q = q & ~Q(pets__contains=choice[0])
            queryset = queryset.filter(q)
        languages = form.cleaned_data['languages']
        if languages:
            q = Q()
            for lang in languages:
                q = q | Q(languages__contains=lang)
            queryset = queryset.filter(q)
        accessability = form.cleaned_data['accessability_needs']
        if accessability != 'null':
            queryset = queryset.filter(accessability_needs__exact=accessability)
        priority = form.cleaned_data['priority']
        if priority:
            q = Q()
            for prio in priority:
                q = q | Q(priority__contains=prio)
            queryset = queryset.filter(q)
        
        state = form.cleaned_data['state']
        if state:
            q = Q()
            for stat in state:
                q = q | Q(state=stat)
            queryset = queryset.filter(q)
        no_handler = form.cleaned_data['no_handler']
        if no_handler:
            queryset = queryset.filter(case_handler__isnull=True)
        handler = form.cleaned_data['case_handler']
        if handler:
            queryset = queryset.filter(case_handler=handler)

        sort = form.cleaned_data['sort']
        direction = '' if  form.cleaned_data['sort_direction'] == 'asc' else '-'
        
        context = {}
        context['dataset'] = queryset.order_by(direction+sort)
        return render(None,'serd/request_list.html', context)

class OfferFilter(FormView):
    template_name = "serd/offer_filter.html"
    form_class = OfferFilterForm
    
    def form_valid(self, form) -> HttpResponse:
        queryset = Offer.objects.all()
        data = form.cleaned_data
        num_min = data['num_min']
        if num_min:
            queryset = queryset.filter(total_number__gte=num_min)
        num_max = data['num_max']
        if num_max:
            queryset = queryset.filter(total_number__lte=num_max)

        plz = data['PLZ']
        if plz:
            queryset = queryset.filter(plz__startswith=plz)
        city = data['city']
        if city:
            queryset = queryset.filter(city__icontains=city)
        cost_min = data['cost_min']
        if cost_min:
            queryset = queryset.filter(cost__gte=cost_min)
        cost_max = data['cost_max']
        if cost_max is not None:
            queryset = queryset.filter(cost__lte=cost_max)
        language = data['language']
        if language:
            q = Q()
            for lang in language:
                q = q | Q(language__contains=lang)
            queryset = queryset.filter(q)
        spontan = data['spontan']
        if spontan != 'null':
            queryset = queryset.filter(spontan__exact=spontan)
        limited = data['limited']
        if limited != 'null':
            queryset = queryset.filter(limited_availability__exact=limited)
        appartment = data['appartment']
        if appartment != 'null':
            queryset = queryset.filter(seperate_appartment__exact=appartment)
        pets = data['pets']
        if pets:
            q = Q()
            for pet in pets:
                q = q & Q(pets__contains=pet)
            queryset = queryset.filter(q)
        accessability = data['accessability']
        if accessability != 'null':
            queryset = queryset.filter(accessability__exact=accessability)
        state = data['state']
        if state:
            q = Q()
            for stat in state:
                q = q | Q(state=stat)
            queryset = queryset.filter(q)
        for_free = data['for_free']
        if for_free != 'null':
            queryset = queryset.filter(for_free__exact=for_free)
        
        sort = form.cleaned_data['sort']
        direction = '' if  form.cleaned_data['sort_direction'] == 'asc' else '-'

        context = {}
        context['dataset'] = queryset.order_by(direction+sort)
        return render(None,'serd/offer_list.html', context)


@login_required
def statistics(request):
    placed_requests = HousingRequest.objects.filter(state='arrived')
    stale_requests = HousingRequest.objects.filter(state='stale')
    persons_placed = placed_requests.aggregate(Sum('persons'))['persons__sum']
    requests_placed = placed_requests.count()
    requests_stale = stale_requests.count()
    persons_stale = stale_requests.aggregate(Sum('persons'))['persons__sum']
    all_requests = HousingRequest.objects.all()
    requests_all =  all_requests.count()
    persons_all = all_requests.aggregate(Sum('persons'))['persons__sum']
    hotel = HousingRequest.objects.filter(hotel__isnull=False).aggregate(Sum('persons'))['persons__sum']
    context = {}
    contact_requests = HousingRequest.objects.filter(state="housing_contact")
    requests_contact = contact_requests.count()
    persons_contact = contact_requests.aggregate(Sum('persons'))['persons__sum']
    city_offers = Offer.objects.filter(by_municipality=True)
    offers_city = city_offers.count()
    offers_city_quasi_placed = city_offers.filter(Q(state='arrived')|Q(state='request_contact')).count()
    context['persons_placed'] = persons_placed
    context['requests_placed'] = requests_placed
    context['persons_stale'] = persons_stale
    context['requests_stale'] = requests_stale
    context['persons_all'] = persons_all
    context['requests_all'] = requests_all
    context['requests_quasi'] = requests_placed + requests_contact
    context['persons_quasi'] = persons_placed + persons_contact
    context['hotel'] = hotel
    context['offers_city'] = offers_city
    context['city_quasi_placed'] = offers_city_quasi_placed
    return render(request, 'serd/statistics.html', context)

@login_required
def profile_view(request, profile_id):
    context = {}
    context['data'] = Profile.objects.get(account__id=profile_id)
    return render(request, 'serd/profile_view.html', context)

@login_required
def profile_list(request):
    context = {}
    context["dataset"] = Profile.objects.all()
    return render(request, "serd/profile_list.html", context)


class UpdateProfile(UpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = "/"
    def get_object(self, queryset=None):
        return Profile.objects.get(account__id=self.request.user.id)
        
        
    
@login_required
def invoice_view(request):
    if request.method =='GET':
        form = InvoiceSelectionForm()
        return render(request, 'serd/invoice_select.html', {'form': form} )
    elif request.method == 'POST':
        context = {}
       
        form = InvoiceSelectionForm(request.POST)
        hotel: Hotel = Hotel.objects.get(number= int(form['hotel'].value()))
        start = datetime.strptime(form['start'].value(), '%d.%m.%Y')
        end = datetime.strptime(form['end'].value(), '%d.%m.%Y')
        current_date = start
        current = 0
        data = []
        while(current_date < end):
            row = {}
            row['date'] = current_date.date()
            checkin_stays = HotelStay.objects.filter(hotel=hotel, arrival_date=current_date)
            checkins = 0
            for stay in checkin_stays:
                checkins += stay.request.adults + stay.request.children
            checkout_stays = HotelStay.objects.filter(hotel=hotel, departure_date=current_date)
            checkouts = 0
            for stay in checkout_stays:
                checkouts += stay.request.adults + stay.request.children
            current += checkins
            current -= checkouts
            row['checkins'] = checkins
            row['checkouts'] = checkouts
            row['current'] = current
            current_date+= timedelta(days=1)
            data.append(row)
        context['form'] = form
        context['hotel'] = hotel.name
        context['data'] = data
        return render(request, 'serd/invoice_display.html', context)
        