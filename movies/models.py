from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Movie(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="movies/")
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    cast = models.TextField()
    description = models.TextField(blank=True, null=True)  # optional
    highlighted = models.BooleanField(default=False)  # This field will be used to mark movies for today

    def __str__(self):
        return self.name

    @staticmethod
    def highlight_today_shows():
        today = datetime.now().date()
        # Fetch all showtimes for today
        showtimes = Showtime.objects.filter(date=today)
        
        for showtime in showtimes:
            # Highlight the associated movie of the showtime
            showtime.movie.highlighted = True
            showtime.movie.save()


class Theater(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='theaters')
    time = models.DateTimeField()

    def __str__(self):
        return f'{self.name} - {self.movie.name} at {self.time}'


class Seat(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.seat_number} in {self.theater.name}'


class Booking(models.Model):
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking by {self.user.username} for {self.seat.seat_number} at {self.theater.name}'


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, default=1)  # Default Theater ID
    time = models.TimeField()
    date = models.DateField()

    def __str__(self):
        return f"{self.movie.name} - {self.theater.name} at {self.time}"


class LiveEvent(models.Model):
    name = models.CharField(max_length=255)  # Event name
    event_date = models.DateTimeField()  # Event date and time
    location = models.CharField(max_length=255)  # Location of the event (could be a venue or city)
    event_type = models.CharField(
        max_length=100, 
        choices=[('concert', 'Concert'), ('sports', 'Sports'), ('theater', 'Theater'), 
                 ('festival', 'Festival'), ('opera', 'Opera')]
    )  # Event type
    description = models.TextField()  # A description of the event

    def __str__(self):
        return self.name
