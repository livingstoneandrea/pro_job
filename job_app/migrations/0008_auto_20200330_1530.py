# Generated by Django 3.0.3 on 2020-03-30 15:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('job_app', '0007_auto_20200330_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employment_details',
            name='employer',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='employment_details',
            name='end_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='employment_details',
            name='job_function',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='employment_details',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
