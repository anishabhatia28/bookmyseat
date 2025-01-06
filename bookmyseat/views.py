from django.shortcuts import render
from django.db import models
from movies.models import Booking, Movie, Theater




def admin_dashboard(request):
    try:
        # Aggregate the total revenue. Make sure your 'Booking' model has a 'ticket_price' field.
        total_revenue = Booking.objects.aggregate(total_revenue=models.Sum('ticket_price'))['total_revenue'] or 0  # Default to 0 if no revenue data
    except KeyError:
        total_revenue = 0  # If no 'ticket_price' field in the model, set revenue to 0

    # Get the top 5 most popular movies based on the number of bookings
    most_popular_movies = Movie.objects.annotate(
        bookings_count=models.Count('booking')
    ).order_by('-bookings_count')[:5]  # Top 5 most popular movies

    # Get the top 5 busiest theaters based on the number of bookings
    busiest_theaters = Theater.objects.annotate(
        bookings_count=models.Count('booking')
    ).order_by('-bookings_count')[:5]  # Top 5 busiest theaters

    # Prepare context for the template
    context = {
        'total_revenue': total_revenue,
        'most_popular_movies': most_popular_movies,
        'busiest_theaters': busiest_theaters,
    }

    # Render the template with the context
    return render(request, 'admin_dashboard.html', context)
