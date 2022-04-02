# import Http Response from django
from dataclasses import fields
from urllib.request import Request

from .models import HousingRequest, Offer
from django.http import HttpResponse

from django.views.generic.edit import CreateView, UpdateView
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
    success_url = "/success"
    form_class = RequestForm

class AddOffer(CreateView):
    model = Offer
    form_class = OfferForm
    success_url ="/success"
   
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

        