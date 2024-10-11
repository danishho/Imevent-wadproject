# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm, EventForm, BookingForm
from .models import CustomUser, Event, Booking
from django.utils import timezone
from django.shortcuts import render, get_object_or_404

def index(request):
    events = Event.objects.filter(start_date__gte=timezone.now()).order_by('start_date')[:4]
    for event in events:
        event.booked_count = Booking.objects.filter(event=event).count()
    return render(request, 'homepage.html', {'events': events})


def register(request):
    if request.method == 'GET':
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            messages.success(request, 'You have signed up successfully.')
            auth_login(request, user)
            return redirect('index')
        else:
            return render(request, 'register.html', {'form': form})


def login(request):

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form,})


    elif request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
                # Authenticate using the user's username and password
                user = authenticate(request, username=user.username, password=password)
                if user:
                    auth_login(request, user)
                    messages.success(request, 'Welcome back!')
                    return redirect('index')  # Ensure you have a URL pattern for 'homepage'

                else:
                    messages.error(request, 'Invalid password.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'User with this email does not exist.')
        else:
            messages.error(request, 'Please provide both email and password.')

        form = LoginForm(request.POST)  # Re-create the form with posted data

        return render(request, 'login.html', {'form': form,})

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')


def createEvent(request):
    if request.method == 'GET':
        form = EventForm()
        return render(request, 'addevent.html', {'form': form, })
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('index')
    return render(request, 'addevent.html')


def event(request):
    events = Event.objects.all()
    for event in events:
        event.booked_count = Booking.objects.filter(event=event).count()
    return render(request, 'event.html', {'events': events})


def eventDetails(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.booked_count = Booking.objects.filter(event=event).count()
    return render(request, 'eventDetails.html', {'event': event})


def book(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'GET':
        user = CustomUser.objects.get(pk=request.user.id)
        form = BookingForm(initial={'phone_number': user.phone_number})
        context = {'event': event, 'user': user, 'form': form}
    if request.method == 'POST':
        if request.method == 'POST':
            form = BookingForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.event = event
                booking.user = request.user  # assuming the user is logged in
                booking.save()
                return redirect('index')  # Redirect to a success page
    return render(request, 'book.html', context)


def myevent(request):
    return None


def yourbooking(request):
    return None