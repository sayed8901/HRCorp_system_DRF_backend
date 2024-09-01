from rest_framework import serializers
from .models import ConfirmationInfo

class ConfirmationInfoSerializer(serializers.ModelSerializer):
    confirmed_designation = serializers.StringRelatedField()
    
    class Meta:
        model = ConfirmationInfo
        fields = '__all__'
        # exclude = ['employee',]

        read_only_fields = ['employee', ]
