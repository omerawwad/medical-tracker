from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule

@shared_task
def send_email_reminder():
    for i in range(5):
        print(f"Reminder {i + 1}: Please take your medication.")

def create_periodic_task():
    schedule, _ = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS)
    PeriodicTask.objects.get_or_create(
        name="Email Reminder",
        task="medical_tracker.tasks.send_email_reminder",
        interval=schedule,
    )