# Generated by Django 5.2.4 on 2025-07-15 19:41

import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_tracker', '0003_medicationreminder'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='medicationreminder',
            unique_together={('user', 'drug', 'reminder_time')},
        ),
        migrations.AlterField(
            model_name='medicationreminder',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Start date for the reminder'),
        ),
    ]
