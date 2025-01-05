from django.core.mail import send_mail

def send_ticket_confirmation(user_email, booking_details):
    subject = 'Your Ticket Booking Confirmation'
    message = f"""
    Dear Customer,

    Your booking has been successfully confirmed. Here are the details:
    {booking_details}

    Thank you for choosing our service!

    Best regards,
    Your Movie Booking Team
    """
    from_email = 'yourname@gmail.com'  # Same email as in settings.py
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
