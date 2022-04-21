"""serd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.conf.urls.i18n import i18n_patterns
from .views import (AddOffer, AddRequest, OfferUpdate, offer_list, request_list, RequestUpdate,  index, SuccessOffer,
                    SuccessRequest, RequestFilter, OfferFilter, hotel_list, OfferAutocomplete)
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),

    path("accounts/", include("django.contrib.auth.urls")),
    path('requests/',request_list, name='requests'),
    path('offers/', offer_list, name='offers'),
    path('offers/edit/<offer_id>', login_required(OfferUpdate.as_view())),
    path('requests/edit/<request_id>', login_required(RequestUpdate.as_view())),
    path('request_filter', login_required(RequestFilter.as_view()), name="request_filter"),
    path('offer_filter', login_required(OfferFilter.as_view()), name="offer_filter"),
    path('',index, name='index'),
    path('hotels/', hotel_list, name='hotels'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('autocomplete-offer', login_required(OfferAutocomplete.as_view()), name='offer-autocomplete'),

   
]
urlpatterns += i18n_patterns(
    path('add_request/',AddRequest.as_view(),name='add_request'),
    path('add_offer/', AddOffer.as_view(), name='add_offer'),
    path('success_request/<request_id>', SuccessRequest.as_view(), name='success_request'),
    path('success_offer/<offer_id>', SuccessOffer.as_view(), name='success_offer')
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
