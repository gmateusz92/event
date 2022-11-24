from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm, EventForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import csv
#import pdf stuff
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import io
# Import Pagination Stuff
from django.core.paginator import Paginator


def index(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = 'John'
    month = month.title()
    # konwersja nazwy miesiaca na liczbe
    month_number = list(calendar.month_name).index(month)
    cal = HTMLCalendar().formatmonth(year, month_number)
    # dzisiejsza data
    now = datetime.now()
    current_year = now.month
    time = now.strftime('%I:%M:%S %p')
    return render(request, 'blog/index.html', {'name':name,
                                               'year':year,
                                               'month':month,
                                               'month_number': month_number,
                                               'cal': cal,
                                               'current_year': current_year,
                                               'time': time
                                               })

def all_events(request):
    event_list = Event.objects.all().order_by('-name')
    return render(request, 'blog/event_list.html', {'event_list':event_list})

def add_venue(request):
    submitted = False #jezeli ktos 1 raz wchodzi na strone to nie wypelnil formularza wiec Falsz
    if request.method == 'POST':
        form = VenueForm(request.POST) #jezeli wypelniono przesyla do form wypelniony formularz (request.POST)
        if form.is_valid(): #jezeli formularz zostal dobrze wypelniony
            venue = form.save(commit=False)
            venue.owner = request.user.id #logged in user
            venue.save()
            #form.save()
            return HttpResponseRedirect('/add_venue?submitted=True') #po zwroceniu strony formularz jest True
    else:
        form = VenueForm
        if 'sumbitted' in request.GET: # jezeli formularz zostal wypelniony wysyla zapytanie GET do strony
            submitted = True
    return render(request, 'blog/add_venue.html', {'form':form, 'submitted':submitted})

def list_venues(request):
    #venue_list = Venue.objects.all().order_by('-name')
    venue_list = Venue.objects.all()
    # Set up Pagination
    p = Paginator(Venue.objects.all(), 2)
    page = request.GET.get('page')
    venues = p.get_page(page)
    # tworzy string (django nie przyjmie int)
    nums = 'a' * venues.paginator.num_pages
    return render(request, 'blog/venue.html', {'venue_list':venue_list, 'venues': venues, 'nums':nums})

def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id) #pobieramy primary key id (kazdy object Venu ma pk id)
    return render(request, 'blog/show_venue.html', {'venue': venue})

def search_venues(request, ):
    if request.method == 'POST':
        searched = request.POST['searched'] #zmienna wypelniajaca formularz w pasku szukania
        venues = Venue.objects.filter(name__contains=searched) #filtruje obiekty klasy Venue w pasku szukania
        return render(request, 'blog/search_venues.html', {'searched':searched, 'venues':venues})
    else:
        return render(request, 'blog/search_venues.html', {})

def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id) #pobieramy primary key id (kazdy object Venu ma pk id)
    form = VenueForm(request.POST or None, instance=venue) # do instance dajemy to co chcemy wrzucic do formularza(widac co jest aktualnie)
    if form.is_valid():  # jezeli formularz zostal dobrze wypelniony
        form.save()
        return redirect('list_venues')
    return render(request, 'blog/update_venue.html', {'venue': venue, 'form':form})

def add_event(request):
    submitted = False #jezeli ktos 1 raz wchodzi na strone to nie wypelnil formularza wiec Falsz
    if request.method == 'POST':
        form = EventForm(request.POST) #jezeli wypelniono przesyla do form wypelniony formularz (request.POST)
        if form.is_valid(): #jezeli formularz zostal dobrze wypelniony
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True') #po zwroceniu strony formularz jest True
    else:
        form = EventForm
        if 'sumbitted' in request.GET: # jezeli formularz zostal wypelniony wysyla zapytanie GET do strony
            submitted = True
    return render(request, 'blog/add_event.html', {'form':form, 'submitted':submitted})

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id) #pobieramy primary key id (kazdy object Venu ma pk id)
    form = EventForm(request.POST or None, instance=event) # do instance dajemy to co chcemy wrzucic do formularza(widac co jest aktualnie)
    if form.is_valid():  # jezeli formularz zostal dobrze wypelniony
        form.save()
        return redirect('all_events')
    return render(request, 'blog/update_event.html', {'event': event, 'form':form})

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('all_events')

def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list_venues')

def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    venues = Venue.objects.all()
    lines = []
    for venue in venues:
        #lines.append('{} {}\n'.format(venue.name, venue.adress, venue.zip_code, venue.phone)) #inny format (f'{venue}\n)
        lines.append(f'{venue.name}\n {venue.adress}\n {venue.zip_code}\n {venue.phone}\n\n\n')
    #Zapisanie do pliku (lines)
    response.writelines(lines)
    return response

def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    #zapisujemy do excela
    writer = csv.writer(response)

    venues = Venue.objects.all()
    #tworzymy kolumny w excelu
    writer.writerow(['Venue Name', "Adress", "Zip code", 'Phone', 'Web adress', 'Email'])

    for venue in venues:
        writer.writerow([venue.name, venue.adress, venue.zip_code, venue.phone])
    return response

# do pdf pip install reportlab trzeba
# Generate a PDF File Venue List
def venue_pdf(request):
    # Create Bytestream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # Add some lines of text
    # lines = [
    #	"This is line 1",
    #	"This is line 2",
    #	"This is line 3",
    # ]

    # Designate The Model
    venues = Venue.objects.all()

    # Create blank list
    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.adress)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_adress)
        lines.append(" ")

    # Loop
    for line in lines:
        textob.textLine(line)

    # Finish Up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    # Return something
    return FileResponse(buf, as_attachment=True, filename='venue.pdf')