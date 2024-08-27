from rest_framework import serializers
from .models import ConfirmationInfo

class ConfirmationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmationInfo
        fields = '__all__'

        read_only_fields = ['employee', ]
