from django.dispatch import receiver
from django.db.models.signals import post_save
from app1.models import Organization, CustomUser


@receiver(post_save, sender=Organization)
def update_user(sender, instance, created, **kwargs):
  if created:
    owner_user = CustomUser.objects.get(id=instance.owner.id)
    if not owner_user.org:
      owner_user.org = Organization.objects.get(id=instance.id)
      owner_user.save()
