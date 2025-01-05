from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Theater, Seat, Booking, Showtime, LiveEvent  # Import necessary models
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from datetime import datetime
from django.utils import timezone
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse


# Function for sending email confirmation after booking
def send_ticket_confirmation_email(booking):
    subject = f"Booking Confirmation for {booking.movie.name}"
    message = render_to_string('ticket_confirmation_email.html', {
        'booking': booking,
        'user': booking.user,
    })

    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.user.email],
    )
    email.content_subtype = "html"  # To send HTML email
    email.send()


# Homepage view for highlighting today's shows
def homepage(request):
    showtime_str = '2025-01-03 18:30:00+00:00'

    # Convert the string to a datetime object
    showtime = datetime.fromisoformat(showtime_str)

    # Prepare the context to send to the template
    context = {
        'showtime': showtime,  # Pass 'showtime' instead of 'event_date'
    }

    # Render the template
    return render(request, 'movies/movie_list.html', context)


# Movie list view with search functionality
def movie_list(request):
    movies = Movie.objects.all()  # Fetch all movies
    return render(request, 'movies/movie_list.html', {'movies': movies})


# Theater list view for a particular movie
def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theaters = Theater.objects.filter(movie=movie)
    return render(request, 'movies/theater_list.html', {'movie': movie, 'theaters': theaters})


@login_required(login_url='/login/')
def book_seats(request, theater_id):
    theater = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater=theater)

    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        error_seats = []

        if not selected_seats:
            return render(request, "movies/seat_selection.html", {
                'theater': theater, 
                'seats': seats, 
                'error': "No seat selected"
            })

        for seat_id in selected_seats:
            seat = get_object_or_404(Seat, id=seat_id, theater=theater)
            if seat.is_booked:
                error_seats.append(seat.seat_number)
                continue

            try:
                booking = Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theater.movie,
                    theater=theater
                )
                seat.is_booked = True
                seat.save()

                # Send email confirmation
                send_ticket_confirmation_email(booking)

            except IntegrityError:
                error_seats.append(seat.seat_number)

        if error_seats:
            error_message = f"The following seats are already booked: {', '.join(error_seats)}"
            return render(request, 'movies/seat_selection.html', {
                'theater': theater, 
                'seats': seats, 
                'error': error_message
            })

        return redirect('profile')

    return render(request, 'movies/seat_selection.html', {
        'theater': theater, 
        'seats': seats
    })




# Today's shows filtered by date
def todays_shows(request):
    today = datetime.today().date()
    # Get today's shows based on the Showtime model
    todays_shows = Showtime.objects.filter(date=today)

    # If no shows for today, you can add a fallback message
    error_message = None
    if not todays_shows:
        error_message = "No shows available for today."

    return render(request, 'movies/todays_shows.html', {"todays_shows": todays_shows, "today": today, "error_message": error_message})


from movies.utils import send_ticket_confirmation

def book_ticket(request):
    # Booking logic here...
    user_email = request.user.email  # Get user email
    booking_details = "Movie: Pushpa\nTheater: NY Cinemas\nSeats: A1, A2"
    
    # Send confirmation email
    send_ticket_confirmation(user_email, booking_details)

    return HttpResponse('Booking confirmed and email sent!')
