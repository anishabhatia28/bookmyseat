from django.contrib import admin
from django.urls import path
from bookmyseat.views import admin_dashboard  # Correct import
from .models import Movie, Theater, Seat, Booking, Showtime
from .models import LiveEvent

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'cast', 'description', 'highlighted']  # Ensure these fields exist in your Movie model
    list_editable = ('highlighted',)
    
@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie', 'time']  # Ensure 'name', 'movie', 'time' exist in the Theater model

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['theater', 'seat_number', 'is_booked']  # Ensure 'theater', 'seat_number', 'is_booked' exist in the Seat model

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'seat', 'movie', 'theater', 'booked_at']  # Ensure these fields exist in the Booking model

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ['movie', 'theater', 'date', 'time']  # Ensure 'movie', 'theater', 'date', 'time' exist in the Showtime model

# Custom admin site with custom dashboard URL
class MyAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('admin_dashboard/', self.admin_view(admin_dashboard)),  # Custom URL for admin dashboard
        ]
        return custom_urls + urls

# Register the custom admin site
admin_site = MyAdminSite(name='myadmin')

@admin.register(LiveEvent)
class LiveEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_date', 'location', 'event_type')  # Ensure these fields exist in the LiveEvent model
    list_filter = ('event_type',)  # Filter events by type (concert, sports, etc.)
    search_fields = ('name', 'location')  # Allow searching by event name and location
    ordering = ('-event_date',)  # Default ordering by event date (descending)
