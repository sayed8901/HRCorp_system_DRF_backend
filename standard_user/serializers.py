from rest_framework import serializers
from .models import StandardUser
from power_user.models import PowerUser

from django.contrib.auth import get_user_model

User = get_user_model()


# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'user_type']


# Serializer for PowerUser model
class PowerUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PowerUser
        fields = ['user',]


# Serializer for StandardUser model
class StandardUserSerializer(serializers.ModelSerializer):
    # to view the user account details too
    user = UserSerializer(read_only=True)

    # Serializing the supervisor (PowerUser) details
    supervisor = PowerUserSerializer(read_only=True)

    class Meta:
        model = StandardUser
        fields = '__all__'


# crating serializer for user registration
class StandardUserRegistrationSerializer(serializers.ModelSerializer):
    contact_no = serializers.CharField(max_length=11)

    supervisor = serializers.PrimaryKeyRelatedField(queryset = PowerUser.objects.all(), write_only = True)

    # The SlugRelatedField will allow to look up the supervisor by their username.
    # supervisor = serializers.SlugRelatedField(
    #     slug_field='user__username',
    #     queryset=PowerUser.objects.all(),
    #     write_only=True
    # )

    confirm_password = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'contact_no', 'email', 'password', 'confirm_password', 'supervisor'
        ]

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        contact_no = self.validated_data['contact_no']

        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        supervisor = self.validated_data['supervisor']

        if password != confirm_password:
            raise serializers.ValidationError({'error' : "Password Doesn't Matched."})
        
        # unique email restriction
        if User.objects.filter(email = email, user_type = 'standard_user').exists():
            raise serializers.ValidationError({'error' : "Email Already Exists."})
        
        account = User(
            username = username, first_name = first_name, last_name = last_name, email = email, 

            # defining user type here
            user_type = 'standard_user',
        )
        print(account)
        account.set_password(password)

        # initially set to False, will be true after activation link validation
        account.is_active = False  

        account.save()

        standard_user_account = StandardUser(
            user = account,
            contact_no = contact_no,
            supervisor = supervisor,
        )

        standard_user_account.save()

        # returning the customUser account of standard_user_account object model to use in the registrationViewSet
        return account
    