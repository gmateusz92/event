from django.contrib import admin
from .models import Venue
from .models import MyClubUser
from .models import Event

#admin.site.register(Venue)
admin.site.register(MyClubUser)
#admin.site.register(Event)

@admin.register(Venue) #zmienia wyglad panelu admina
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'adress', 'phone') # dodaje kolumny
    ordering = ('name',) # sortuje wg alfabetu, jak - to odwrotnie
    search_fields = ('name', 'adress') #pasek szukania

@admin.register(Event)
class VenueEvent(admin.ModelAdmin):
    fields = ('name', 'venue', 'event_date', 'description', 'manager') # np (('name', 'venue')) tulpe i w jednej lini wyswietla
    list_display = ('name','event_date', 'venue') # dodaje kolumny
    list_filter = ('event_date', 'venue') # dodaje filtry z prawej strony
    ordering = ('-event_date',)