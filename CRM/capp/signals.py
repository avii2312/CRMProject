from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Ticket, Project, Client
from accounts.middleware import get_current_user

@receiver(pre_save, sender=Ticket)
def ticket_audit(sender, instance, **kwargs):
    user = get_current_user()
    if instance._state.adding:
        instance.created_by = user
    instance.updated_by = user

# Repeat for Project and Client
