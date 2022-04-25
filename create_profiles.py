#!/usr/bin/env python3
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "serd.settings")
django.setup()
from django.contrib.auth import get_user_model
from serd.models import Profile

User = get_user_model()
users = User.objects.all()
for user in users:
    profile = Profile()
    profile.number = user.pk
    profile.name = user.first_name
    profile.whatsapp = True
    profile.signal = False
    profile.account = user
    profile.save()