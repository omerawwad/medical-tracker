from django.shortcuts import render
from rest_framework import generics
from .models import Drug, MedicationReminder
from .serializers import DrugSerializer, MedicationReminderSerializer
# from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework import filters
from .filters import MyOrderingFilter 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .tasks import create_periodic_task, send_email_reminder, analyze_file

@method_decorator(cache_page(60 * 15, key_prefix="drug_list"), name='dispatch')
class DrugListAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve and create drugs.
    """
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # pagination_class = LimitOffsetPagination
    ordering_fields = ['name', 'dosage_type']
    ordering = ['name']
    filter_backends = [filters.SearchFilter, MyOrderingFilter]
    search_fields = ['name', 'description', 'dosage_type']

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    def get_permissions(self):
        if self.request.method != 'GET':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    

# class DrugDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

class MedicationReminderListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve and create medication reminders.
    """
    queryset = MedicationReminder.objects.prefetch_related('drug').all()
    serializer_class = MedicationReminderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # send_email_reminder.delay()
        # create_periodic_task()
        analyze_file.delay(file_id="24680", data="Seventh example of file data to analyze")
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
