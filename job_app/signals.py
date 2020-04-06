from django.db.models.signals import post_save
from django.contrib.auth.models import User
from job_app.models import Profile
from django.dispatch import receiver


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print("profile created")
    instance.profile.save()
    print("profile updated")