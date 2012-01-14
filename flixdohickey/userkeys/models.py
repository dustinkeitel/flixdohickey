from django.db import models
from django.contrib.auth.models import User
from django.db.models import OneToOneField, CharField, BooleanField

class UserKeys(models.Model):
    user = OneToOneField('auth.User')
    request_key = CharField()
    request_secret = CharField()
    access_key = CharField()
    access_secret = CharField()
    