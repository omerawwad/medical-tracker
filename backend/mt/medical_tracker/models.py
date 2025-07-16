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
    


class MedicalFile(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='medical_files', null=False, blank=False)
    visible = models.BooleanField(default=True)
    archived = models.BooleanField(default=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    file_date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    source = models.CharField(max_length=100, null=True, blank=True, help_text='Source of the medical file (e.g., hospital, clinic)')

    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['owner'], name='medical_file_user_idx'),
        ]

    def __str__(self):
        return f'Medical file {self.id} for {self.owner.username}'

def file_path(instance, filename):
    return f'users_files/{instance.file.owner.username}/{instance.file.id}/{filename}'

class FileImage(models.Model):
    file = models.ForeignKey(MedicalFile, on_delete=models.CASCADE, related_name='images', null=False, blank=False)
    image = models.ImageField(upload_to=file_path, null=False, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    @property
    def image_size(self):
        return self.image.size if self.image else 0
    @property
    def image_url(self):
        return self.image.url if self.image else None
    @property
    def image_extension(self):
        return self.image.name.split('.')[-1] if self.image else None
    
    def __str__(self):
        return f'Image for {self.file.title} uploaded at {self.uploaded_at}, image size: {self.image_name} bytes'