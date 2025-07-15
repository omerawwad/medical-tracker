from django.urls import path
from . import views

urlpatterns = [
    path('drugs/', views.DrugListAPIView.as_view(), name='drugs'),
    path('medication-reminders/', views.MedicationReminderListCreateAPIView.as_view(), name='medication-reminders'),
]