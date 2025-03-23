from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Board, List

@receiver(post_save, sender=Board)
def create_default_lists(sender, instance, created, **kwargs):
    if created:
        default_lists = ["To Do", "Doing", "Suspend", "Done"]
        for list_name in default_lists:
            List.objects.create(name=list_name, board=instance)