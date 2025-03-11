from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Notification
from chat.models import Message

@receiver(post_save, sender=None)
def booking_notification(sender, instance, created, **kwargs):
    from booking.models import Booking 

    if isinstance(instance, Booking) and created:
        Notification.objects.create(
            recipient=instance.expert,  
            description=f'Новый запрос на консультацию от: {instance.user.first_name} {instance.user.last_name}',
            link=f'/booking/my_bookings'
        )

@receiver(post_save, sender=Message)
def message_notification(sender, instance, created, **kwargs):
    if created:
        recipient = instance.chat.get_chat_partner(instance.sender)
        if recipient:
            Notification.objects.create(
                recipient=recipient,
                description=f'Новое сообщение от: {instance.sender.first_name} {instance.sender.last_name}',
                link=f'/chat/{instance.chat.id}'
            )

