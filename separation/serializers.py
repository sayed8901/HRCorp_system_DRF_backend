from rest_framework import serializers
from .models import SeparationInfo

class SeparationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeparationInfo
        fields = '__all__'
        # exclude = ['employee',]

        read_only_fields = ['employee', ]
