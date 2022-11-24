from django.db import models
from django.contrib.auth.models import User #nadaje uprawanienia admina do dodawania eventów

class Venue(models.Model):
    name = models.CharField('Event name', max_length=120)
    adress = models.CharField( max_length=120)
    zip_code = models.CharField('Zip_code', max_length=120)
    phone = models.CharField('Phone', max_length=120, blank=True)
    web = models.URLField('Website adress', max_length=120, blank=True)
    email_adress = models.EmailField('Email', max_length=120, blank=True)
    owner = models.IntegerField('Venue owner', blank=False, default=1) #int poniewaz uzytkownik ma id

    def __str__(self):
        return self.name

class MyClubUser(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email_adress = models.EmailField('Email', max_length=120)

    def __str__(self):
        return self.first_name + '' + self.last_name

class Event(models.Model):
    name = models.CharField('Event name', max_length=120)
    event_date = models.DateTimeField()
    venue = models.ForeignKey(Venue, blank = True, null=True, on_delete=models.CASCADE) # lączy jeden z wieloma
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL) #nadaje uprawanienia admina do dodawania eventów
    description = models.CharField(max_length=1200)
    attendes = models.ManyToManyField(MyClubUser, blank=True) #wielu uczestnikow moze brac udzial w wielu eventach

    def __str__(self):
        return self.name







