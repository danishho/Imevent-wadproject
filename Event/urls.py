from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('createEvent/', views.createEvent, name='createEvent'),
    path('event/', views.event, name='event'),
    path('event/<int:event_id>', views.eventDetails, name='eventDetails'),
    path('book/<int:event_id>', views.book, name='book'),
    path('myevent/', views.myevent, name='myevent'),
    path('yourbooking/', views.yourbooking, name='yourbooking'),
]