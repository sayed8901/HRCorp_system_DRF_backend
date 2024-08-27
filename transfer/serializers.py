from rest_framework import serializers
from .models import TransferInfo
from employment.models import JobLocation, Department


class TransferInfoSerializer(serializers.ModelSerializer):
    # SlugRelatedField uses a field (slug_field) to map names to instances.
    # 'queryset' allows the serializer to look up Location and Department instances by name.

    transfer_from_location = serializers.SlugRelatedField(
        slug_field='name',
        queryset=JobLocation.objects.all()
    )
    transfer_to_location = serializers.SlugRelatedField(
        slug_field='name',
        queryset=JobLocation.objects.all()
    )
    transfer_from_department = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Department.objects.all()
    )
    transfer_to_department = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Department.objects.all()
    )


    class Meta:
        model = TransferInfo
        fields = '__all__'

        read_only_fields = ['employee', ]


