from rest_framework import serializers
from .models import Drug, MedicationReminder
class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ['id', 'name', 'description', 'dosage_type']
        read_only_fields = ['id']

class MedicationReminderSerializer(serializers.ModelSerializer):
    drug = DrugSerializer(read_only=True)
    drug_id = serializers.UUIDField(write_only=True, help_text='ID of the drug for which the reminder is set')
    user = serializers.CharField(source='user.username', read_only=True, help_text='Username of the user setting the reminder')
    
    class Meta:
        model = MedicationReminder
        fields = ['id', 'user', 'drug', 'drug_id', 'start_date', 'reminder_time', 'number_of_doses', 'end_date']
        read_only_fields = ['id', 'user']
        extra_kwargs = {
            
            'reminder_time': {'required': False, 'default': MedicationReminder.ReminderTime.AFTER_WAKE_UP},
            'number_of_doses': {'required': False, 'allow_null': True},
            'end_date': {'required': False, 'allow_null': True}
        }

    def validate(self, attrs):
        if 'end_date' in attrs and attrs['end_date'] < attrs['start_date']:
            raise serializers.ValidationError("End date cannot be before start date.")
        if 'number_of_doses' in attrs and attrs['number_of_doses'] <= 0:
            raise serializers.ValidationError("Number of doses must be a positive integer.")
        if 'drug_id' not in attrs:
            raise serializers.ValidationError("Drug must be specified.")
        if MedicationReminder.objects.filter(user=self.context['request'].user, drug_id=attrs['drug_id'], reminder_time=attrs['reminder_time']).exists():
            raise serializers.ValidationError("You already have a reminder for this drug.")
        return attrs
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
