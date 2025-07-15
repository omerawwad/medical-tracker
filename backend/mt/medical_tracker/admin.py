from django.contrib import admin
from .models import Drug, MedicationReminder

admin.site.site_header = "Medical Tracker Admin"
admin.site.site_title = "Medical Tracker Admin Portal"
# admin.site.index_title = "Welcome to the Medical Tracker Admin Portal"

admin.site.register(Drug)
admin.site.register(MedicationReminder)
