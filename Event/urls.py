from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('accounts/login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('createEvent/', views.createEvent, name='createEvent'),
    path('event/', views.event, name='event'),
    path('search/', views.search, name='search'),
    path('event/<int:event_id>', views.eventDetails, name='eventDetails'),
    path('book/<int:event_id>', views.book, name='book'),
    path('myevent/', views.myevent, name='myevent'),
    path('yourbooking/', views.yourbooking, name='yourbooking'),
    path('updateEvent/<int:event_id>', views.update_event, name='update_event'),
    path('deleteEvent/<int:event_id>', views.delete_event, name='delete_event'),
    path('cancelBooking/<int:booking_id>', views.cancel_booking, name='cancel_booking'),
    path('editProfile/<int:user_id>', views.edit_profile, name='edit_profile'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('delete_user/<int:user_id>', views.delete_user, name='delete_user'),
    path('update_user/<int:user_id>', views.update_user, name='update_user'),
]