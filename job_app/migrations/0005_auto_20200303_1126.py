# Generated by Django 3.0.3 on 2020-03-03 11:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('job_app', '0004_auto_20200301_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education_level',
            name='issue_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='employment_details',
            name='current_job_status',
            field=models.CharField(choices=[('not employed', 'Not Employed'), ('employed', ' Employed')], max_length=20),
        ),
    ]