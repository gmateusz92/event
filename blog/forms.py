from django import forms
from django.forms import ModelForm
from .models import Venue, Event


# tworze formularz
class VenueForm(ModelForm):
    class Meta:  # zawsze dajemy ta klase (definiuje cos tam xd)
        model = Venue  # dzieki temu pobieramy wszystko z klasy Venu
        fields = ('name', 'adress', 'zip_code', 'phone',  'web', 'email_adress') #pobieram pola z klasy Venu
        labels = {
            'name': '',
            'adress': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email_adress': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'adress': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Date'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manager'}),
            'web': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Attendees'}),
            'email_adress': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }


class EventForm(ModelForm):
    class Meta:  # zawsze dajemy ta klase (definiuje cos tam xd)
        model = Event  # dzieki temu pobieramy wszystko z klasy Venu
        fields = ('name', 'event_date', 'venue', 'manager', 'attendes', 'description')  # pobieram pola z klasy Venu
        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS',
            'venue': 'venue',
            'manager': 'manager',
            'attendes': 'attendes',
            'description': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Date'}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            'manager': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Manager'}),
            'attendes': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'attendes'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'description'}),
        }



