from django.urls import path
from . import views

urlpatterns = [
    path('drugs/', views.DrugListAPIView.as_view(), name='drugs'),
    path('medication-reminders/', views.MedicationReminderListCreateAPIView.as_view(), name='medication-reminders'),
    path('medical-files/', views.MedicalFileListCreateAPIView.as_view(), name='medical-files'),
    path('upload-file-image/', views.FileImageUploadAPIView.as_view(), name='upload-file-image'),
] 