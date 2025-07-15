import uuid
from django.db import models
from django.utils import timezone

class Drug(models.Model):
    class DrugDosageType(models.TextChoices):
        TABLET = 'Tablet', 'Tablet'
        CAPSULE = 'Capsule', 'Capsule'
        LIQUID = 'Liquid', 'Liquid'
        INJECTION = 'Injection', 'Injection'
        OINTMENT = 'Ointment', 'Ointment'

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    description = models.TextField()
    dosage_type = models.CharField(max_length=50, choices=DrugDosageType.choices, default=DrugDosageType.TABLET)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'], name='drug_name_idx'),
            models.Index(fields=['dosage_type'], name='drug_dosage_type_idx'),
        ]

    def __str__(self):
        return self.name
    
class MedicationReminder(models.Model):
    class ReminderTime(models.TextChoices):
        AFTER_WAKE_UP = 'after_wake_up', 'After wake up'
        BEFORE_BREAKFAST = 'before_breakfast', 'Before breakfast'
        AFTER_BREAKFAST = 'after_breakfast', 'After breakfast'
        BEFORE_LUNCH = 'before_lunch', 'Before lunch'
        AFTER_LUNCH = 'after_lunch', 'After lunch'
        BEFORE_DINNER = 'before_dinner', 'Before dinner'
        AFTER_DINNER = 'after_dinner', 'After dinner'
        BEFORE_SLEEP = 'before_sleep', 'Before sleep'

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='medication_reminders', null=False, blank=False)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='reminders', null=False, blank=False)
    
    start_date = models.DateTimeField(default=timezone.now, null=False, blank=False, help_text='Start date for the reminder')
    reminder_time = models.CharField(max_length=50, choices=ReminderTime.choices, default=ReminderTime.AFTER_WAKE_UP)
    
    number_of_doses = models.PositiveIntegerField(null=True, blank=True, help_text='Total number of doses')

    class Meta:
        ordering = ['start_date', 'reminder_time']
        unique_together = ('user', 'drug', 'reminder_time')

    @property
    def end_date(self):
        if self.number_of_doses is not None:
            return self.start_date + timezone.timedelta(days=self.number_of_doses - 1)
        return None
    def __str__(self):
        return f'Reminder for {self.drug.name} at {self.reminder_time} for {self.user.username}, starting {self.start_date}'