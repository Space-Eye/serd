# import Http Response from django
from django.urls import reverse

from serd.choices import PETS
from .models import Hotel, HousingRequest, Offer
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView, FormView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import OfferEditForm, OfferForm, RequestEditForm, RequestFilterForm, RequestForm, OfferFilterForm
import datetime

def success(request):
    return HttpResponse("success")

@login_required
def index(request):
    return render(request, "serd/index.html")


class AddRequest(CreateView):
    model = HousingRequest
    form_class = RequestForm
    def get_success_url(self) -> str:
        return reverse('success_request', args=(self.object.number,))


class AddOffer(CreateView):
    model = Offer
    form_class = OfferForm
    
    def get_success_url(self) -> str:

        return reverse('success_offer', args=(self.object.number,))

   
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
    context = {}
    context["dataset"] = Hotel.objects.all()
    return render(request, "serd/hotel_list.html", context)

class OfferUpdate(UpdateView):
    success_url = "/offers"
    def get_object(self, queryset=None):
        return Offer.objects.get(number=self.kwargs["offer_id"])
    form_class = OfferEditForm

class RequestUpdate(UpdateView):
    success_url = "/requests"
    def get_object(self, queryset=None):
        return HousingRequest.objects.get(number=self.kwargs["request_id"])
    form_class = RequestEditForm

        
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
            queryset = queryset.filter(persons__lte=num_min)
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

        context = {}
        context['dataset'] = queryset
        return render(None,'serd/request_list.html', context)

class OfferFilter(FormView):
    template_name = "serd/offer_filter.html"
    form_class = OfferFilterForm
    
    def form_valid(self, form) -> HttpResponse:
        queryset = Offer.objects.all()
        data = form.cleaned_data

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
        context = {}
        context['dataset'] = queryset
        return render(None,'serd/offer_list.html', context)

