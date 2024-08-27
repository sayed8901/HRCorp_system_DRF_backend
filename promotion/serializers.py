from rest_framework import serializers
from .models import PromotionInfo

class PromotionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionInfo
        fields = '__all__'

        read_only_fields = ['employee', ]
