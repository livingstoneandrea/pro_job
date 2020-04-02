from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# Create your models here.


class Employment_details(models.Model):
    employer = models.CharField(max_length=150, blank=True, null=True)
    job_function = models.CharField(max_length=100, blank=True, null=True)
    JOB_STATUS = (
        ('not employed', 'Not Employed'),
        ('employed', ' Employed')

    )

    current_job_status = models.CharField(max_length=20, choices=JOB_STATUS, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s" % (self.employer)


class Education_level(models.Model):
    certification = models.CharField(max_length=100, null=True)
    issuing_org = models.CharField(max_length=100, null=True)
    identification_number = models.CharField(max_length=100)
    issue_date = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.certification


class Preference(models.Model):
    job_field_pref = models.CharField(max_length=100, null=True)
    location_pref = models.CharField(max_length=100, null=True)

    def __str__(self):
        return "%s".format(self.job_field_pref)


class File_uploaded(models.Model):
    file_name = models.CharField(max_length=60, null=True)
    submitted_date = models.DateTimeField(default=timezone.now)
    comments = models.TextField()

    def __str__(self):
        return self.file_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    employment_details = models.ForeignKey(Employment_details, on_delete=models.CASCADE, blank=True, null=True)
    education_level = models.ForeignKey(Education_level, on_delete=models.CASCADE, blank=True, null=True)
    Preference = models.ForeignKey(Preference, on_delete=models.CASCADE, blank=True, null=True)
    file_upload = models.ForeignKey(File_uploaded, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print("profile created")
    instance.profile.save()
    print("profile updated")
