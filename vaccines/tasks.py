from celery import shared_task
from django.core.mail import send_mail
from .models import Appointment


@shared_task
def send_confirmation_email(appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    print('done')
    send_mail(
        'Appointment Confirmation',
        f'You have booked an appointment for {appointment.vaccine.name} on {appointment.date}.',
        'info@ksavaccine.com',
        [appointment.email],
        fail_silently=False,
    )

