from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment
from django.core.mail import send_mail


# @receiver(post_save, sender=Appointment)
# def send_confirmation_email(sender, instance, created, **kwargs):
#     if created:
#         send_mail(
#             'Appointment Confirmation',
#             f'You have booked an appointment for {instance.vaccine.name} on {instance.date}.',
#             'info@ksavaccine.com',
#             [instance.email],
#             fail_silently=False,
#         )
