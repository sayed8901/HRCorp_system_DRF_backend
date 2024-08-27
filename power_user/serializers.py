from rest_framework import serializers
from .models import PowerUser

from django.contrib.auth import get_user_model

User = get_user_model()


# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'user_type']


# Serializer for PowerUser model
class PowerUserSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(many=False)
    
    # to view the user account details too
    user = UserSerializer(read_only=True)

    class Meta:
        model = PowerUser
        fields = '__all__'



# crating serializer for user registration
class PowerUserRegistrationSerializer(serializers.ModelSerializer):
    contact_no = serializers.CharField(max_length=11)
    confirm_password = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'contact_no', 'email', 'password', 'confirm_password'
        ]

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        contact_no = self.validated_data['contact_no']

        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({'error' : "Password Doesn't Matched."})
        
        # unique email restriction
        if User.objects.filter(email = email, user_type = 'power_user').exists():
            raise serializers.ValidationError({'error' : "Email Already Exists."})
        
        account = User(
            username = username, first_name = first_name, last_name = last_name, email = email, 

            # defining user type here
            user_type = 'power_user',
        )
        print(account)
        account.set_password(password)

        # initially set to False, will be true after activation link validation
        account.is_superuser = False
        account.is_active = False  

        account.save()

        power_user_account = PowerUser(
            user = account,
            contact_no = contact_no,
        )

        power_user_account.save()

        # returning the customUser account of power_user_account object model to use in the registrationViewSet
        return account
    