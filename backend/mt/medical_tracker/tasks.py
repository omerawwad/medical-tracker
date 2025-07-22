from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from pymongo import MongoClient
import os
from .models import FileImage, MedicalFile
from django.conf import settings
import openai

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

@shared_task
def analyze_file_task(file_id):
    file = FileImage.objects.get(id=file_id)
    print("=================")
    print(file)
    file.status = FileImage.ImageStatus.PROCESSING
    file.save(update_fields=['status'])

    parent_file_id = file.file
    file_path = os.path.join(settings.MEDIA_ROOT, file.image_url)
    print(f"Analyzing file: {file_path}")

    try:
        with open(file_path, "rb") as f:
            image_bytes = f.read()


        openai.api_key = os.getenv('OPENAI_API_KEY')
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract all the medical test data in structured JSON format."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_bytes.encode('base64')}"}}
                    ]
                }
            ],
            max_tokens=1500
        )

        # Extract and parse result
        result_json = response.choices[0].message['content']

        # Save to MongoDB
        client = MongoClient(os.getenv('MONGO_URI'))
        db = client[os.getenv('MONGO_CLIENT_NAME')]
        collection = db[os.getenv('MONGO_DB_NAME')]
        collection.insert_one({
            "file_id": str(parent_file_id),
            "parsed_data": result_json,
        })

        file.status = FileImage.ImageStatus.PROCESSED
        file.save(update_fields=['status'])

    except Exception as e:
        file.status = FileImage.ImageStatus.FAILED
        file.save(update_fields=['status'])
        raise e

    return "Success"