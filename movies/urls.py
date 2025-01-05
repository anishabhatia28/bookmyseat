from django.urls import path
from . import views
from .admin import admin_site

urlpatterns = [
    # Define the homepage path correctly (Choose the right view)
    path('', views.homepage, name='home'),

    # Movie and Theater paths
    path('movies/', views.movie_list, name='movie_list'),
    path('<int:movie_id>/theaters/', views.theater_list, name='theater_list'),
    
    # Booking path
    path('theater/<int:theater_id>/seats/book/', views.book_seats, name='book_seats'),
    
    # Today's shows path
    path('todays-shows/', views.todays_shows, name='todays_shows'),
    
    # Admin path
    path('admin/', admin_site.urls),
]
