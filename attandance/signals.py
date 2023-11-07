import django.dispatch
from django.dispatch import Signal

order_status_changed = Signal()
received_status_changed = Signal()