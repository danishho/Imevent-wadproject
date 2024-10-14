# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm, EventForm, BookingForm, CustomUserChangeForm, CustomPasswordChangeForm
from .models import CustomUser, Event, Booking
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.db.models import Q



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
            form.save_m2m()
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
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.event = event
            booking.user = request.user  # assuming the user is logged in
            booking.save()
            return redirect('index')  # Redirect to a success page
    return render(request, 'book.html', context)


def myevent(request):
    events = Event.objects.filter(created_by=request.user.id)
    for event in events:
        event.booked_count = Booking.objects.filter(event=event).count()
    return render(request, 'myevent.html', {'events': events})


def yourbooking(request):
    bookings = Booking.objects.select_related('event').filter(user_id=request.user.id)
    return render(request, 'yourbooking.html', {'bookings': bookings})



def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'GET':
        form = EventForm()
        form = EventForm(initial={'title': event.title, 'image': event.image, 'description': event.description,
                                  'location': event.location, 'start_date': event.start_date,
                                  'end_date': event.end_date, 'max_tickets': event.max_tickets})
        return render(request, 'updateEvent.html', {'form': form, })
    # this put
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('myevent')

    return render(request, 'myevent.html')


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('myevent')


def cancel_booking(request,booking_id):
    booking = Booking.objects.get(pk=booking_id)
    booking.delete()
    return redirect('yourbooking')


def edit_profile(request, user_id):
    profile = CustomUserChangeForm(instance=request.user)
    password = CustomPasswordChangeForm(user=request.user)

    if request.method == 'GET':
        return render(request, 'editprofile.html', {"user": profile, "password": password})

    elif request.method == 'POST':
        if 'save_profile' in request.POST:  # Check if profile form is submitted
            profile = CustomUserChangeForm(request.POST, instance=request.user)
            if profile.is_valid():
                profile.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('index')
            else:
                for field, errors in profile.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")

        elif 'change_password' in request.POST:  # Check if password form is submitted
            password = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if password.is_valid():
                user = password.save()
                update_session_auth_hash(request, user)  # Important to prevent logout
                messages.success(request, "Your password was changed successfully!")
                return redirect('index')
            else:
                for field, errors in password.errors.items():
                    for error in errors:
                        messages.error(request, error)

    return render(request, 'editprofile.html', {"user": profile, "password": password})


def search(request):
    query = request.GET.get('q', '')
    events = Event.objects.filter(
        Q(title__icontains=query) | Q(tags__name__icontains=query)
    ).distinct()
    event_data = []
    for event in events:
        booked_count = Booking.objects.filter(event=event).count()
        tags = list(event.tags.values_list('name', flat=True))
        event_data.append({
            'id': event.id,
            'title': event.title,
            'location': event.location,
            'start_date': event.start_date.strftime('%d/%m/%Y'),
            'end_date': event.end_date.strftime('%d/%m/%Y'),
            'booked_count': booked_count,
            'max_tickets': event.max_tickets,
            'image_url': event.image.url if event.image else None,
            'tags': tags,
        })
    return JsonResponse(event_data, safe=False)