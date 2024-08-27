from rest_framework import serializers
from .models import SeparationInfo

class SeparationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeparationInfo
        fields = '__all__'

        read_only_fields = ['employee', ]
