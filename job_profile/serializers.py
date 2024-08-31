from rest_framework import serializers
from .models import JobProfileHistory

class JobProfileHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProfileHistory
        fields = '__all__'
        # exclude = ['employee',]

        read_only_fields = ['employee', ]
