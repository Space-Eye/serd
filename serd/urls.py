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

from .views import AddOffer, AddRequest, OfferUpdate, offer_list, request_list, RequestUpdate, success, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_request/',AddRequest.as_view(),name='add_request'),
    path('add_offer/', AddOffer.as_view(), name='add_offer'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('requests/',request_list, name='requests'),
    path('offers/', offer_list, name='offers'),
    path('offers/edit/<offer_id>', OfferUpdate.as_view()),
    path('requests/edit/<request_id>', RequestUpdate.as_view()),
    path('success', success),
    path('',index)

]

