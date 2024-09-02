from rest_framework import serializers
from .models import SeparationInfo


class SeparationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeparationInfo

        fields = ['employee', 'application_submission_date', 'separation_effect_date', 'cause_of_separation', 'separation_type', ]

        # fields = '__all__'
        # exclude = ['employee',]

        read_only_fields = ['employee', ]
