from django.contrib import admin
from job_app.models import Profile,Employment_details,Education_level,Preference,File_uploaded

# Register your models here.
admin.site.register(Profile)
admin.site.register(Employment_details)
admin.site.register(Education_level)
admin.site.register(Preference)
admin.site.register(File_uploaded)