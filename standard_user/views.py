from django.shortcuts import render, redirect
from rest_framework import viewsets, status

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsStandardUserOrReadOnly, IsStandardUser

from .models import StandardUser
from .serializers import StandardUserSerializer, StandardUserRegistrationSerializer


# necessary importing for confirmation link generating
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.utils.encoding import force_bytes

# to implement email sending functionality
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


from accounts.models import CustomUser

User = get_user_model()




# Create your views here.
class StandardUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsStandardUserOrReadOnly]

    queryset = StandardUser.objects.all()
    serializer_class = StandardUserSerializer




# Creating user registration functionality
class StandardUserRegistrationAPIView(APIView):
    serializer_class = StandardUserRegistrationSerializer

    def post(self, request):
        # form er moto kore 'serialized_data' nie nilam
        serialized_data = self.serializer_class(data = request.data)

        if serialized_data.is_valid():
            user = serialized_data.save()
            print(user)


            # creating a token for the user
            token = default_token_generator.make_token(user)
            print('token :', token)

            # creating an unique url by using the decoded string of the users unique user id such as 'pk' 
            user_id = urlsafe_base64_encode(force_bytes(user.pk))
            print('user_id :', user_id)

            # creating a confirm link (using local domain)
            confirm_link = f'http://127.0.0.1:8000/standard_user/active/{user_id}/{token}/'
            
            # creating a confirm link (using live DRF domain)
            # confirm_link = f'https://hrcorp-system.onrender.com/standard_user/active/{user_id}/{token}/'
            


            # email sending implementation
            email_subject = 'Confirm Your Account'
            email_body = render_to_string('standard_user_confirm_email.html', {
                'user': user,
                'confirm_link': confirm_link,
            })

            email = EmailMultiAlternatives(email_subject, '', to = [user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()


            return Response({'message': 'Check your mail for confirmation.'}, status=status.HTTP_201_CREATED)


        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)





# creating a function to decode the confirmation link for activating the user account
def activate(request, user_id, token):
    try:
        user_id = urlsafe_base64_decode(user_id).decode()
        user = CustomUser._default_manager.get(pk = user_id)
    except(CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # setting up the super user authorization & make the user as active
        user.is_superuser = True
        user.is_active = True
        user.save()
        return redirect('user_login')
    else:
        # er age response ba kono error message die deowa jete pare
        return redirect('standard_user_register')





# to get the specific standard_user object data by an user_id
class StandardUserDataByUserIDView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = StandardUser.objects.get(user=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        
        serializer = StandardUserSerializer(user)
        print('user:', serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

