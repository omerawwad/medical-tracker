from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from pymongo import MongoClient
import os

@shared_task
def send_email_reminder():
    for i in range(5):
        print(f"Reminder {i + 1}: Please take your medication.")

@shared_task
def analyze_file(file_id, data):
    result = {
        "file_id": file_id,
        "metadata": data.upper(),
        "status": "success",
        "message": "File analysis completed successfully."
    }
    client = MongoClient(os.getenv('MONGO_URI'))
    db = client[os.getenv('MONGO_CLIENT_NAME')]
    collection = db[os.getenv('MONGO_DB_NAME')]

    insert_result = collection.insert_one(result)

    return {
        "mongo_id": str(insert_result.inserted_id),
        "message": "Saved successfully"
    }
def create_periodic_task():
    schedule, _ = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS)
    PeriodicTask.objects.get_or_create(
        name="Email Reminder",
        task="medical_tracker.tasks.send_email_reminder",
        interval=schedule,
    )