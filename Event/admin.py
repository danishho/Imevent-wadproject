from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomAdminUserChangeForm
from .models import CustomUser, Event, Booking , Tag


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomAdminUserChangeForm
    model = CustomUser
    list_display = ["email", "username", "user_type", "is_staff", "is_superuser"]
    # Allow admin to change user_type in both the change form and when adding a new user
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'phone_number')}),
    )

    # Include user_type when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type','phone_number')}),
    )


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'start_date', 'end_date', 'max_tickets', 'get_tags', 'created_by']
    list_filter = ['start_date', 'end_date', 'created_by', 'tags']
    search_fields = ['title', 'location']
    readonly_fields = ['created_by']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user  # Automatically set the creator to the logged-in user
        super().save_model(request, obj, form, change)

    def get_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    get_tags.short_description = 'Tags'

class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'booking_date']
    list_filter = ['booking_date', 'event']
    search_fields = ['user__username', 'event__title']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Tag, TagAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Booking, BookingAdmin)