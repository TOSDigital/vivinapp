from django.dispatch import receiver
from .signals import order_status_changed, received_status_changed
from django.core.mail import send_mail

@receiver(order_status_changed)
def send_order_status_notification(sender, instance, **kwargs):
    # Logic to send notification to the site user
    # Add your actual email sending logic here
    send_mail(
        'Order Status Changed',
        f'The order status for indent {instance.indent_no} has been updated.',
        'from@example.com',
        ['siteuser@example.com'],
        fail_silently=False,
    )

@receiver(received_status_changed)
def send_received_status_notification(sender, instance, **kwargs):
    # Logic to send notification to the office user
    # Add your actual email sending logic here
    send_mail(
        'Received Status Changed',
        f'The received status for indent {instance.indent_no} has been updated.',
        'from@example.com',
        ['officeuser@example.com'],
        fail_silently=False,
    )