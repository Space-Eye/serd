# import Http Response from django
from urllib.request import Request
from django.urls import reverse
from .models import HousingRequest, Offer
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import OfferEditForm, OfferForm, RequestEditForm, RequestForm
import datetime

def success(request):
    return HttpResponse("success")

def index(request):
    return render(request, "serd/index.html")


class AddRequest(CreateView):
    model = HousingRequest
    form_class = RequestForm
    def get_success_url(self) -> str:
        return reverse('success_request', args=(self.object.id,))

def add_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/success_request/')

    else:
        form = RequestForm()

    return render(request, 'name.html', {'form': form})  

class AddOffer(CreateView):
    model = Offer
    form_class = OfferForm
    
    def get_success_url(self) -> str:

        return reverse('success_offer', args=(self.object.id,))

   
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
   

class OfferUpdate(UpdateView):
    success_url = "/offers"
    def get_object(self, queryset=None):
        return Offer.objects.get(id=self.kwargs["offer_id"])
    form_class = OfferEditForm

class RequestUpdate(UpdateView):
    success_url = "/requests"
    def get_object(self, queryset=None):
        return HousingRequest.objects.get(id=self.kwargs["request_id"])
    form_class = RequestEditForm

        
class SuccessOffer(TemplateView):
    template_name = "serd/success_offer.html"
  

class SuccessRequest(TemplateView):
    template_name = "serd/success_request.html"
  
