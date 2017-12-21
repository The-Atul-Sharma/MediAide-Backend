import datetime
from datetime import timedelta
import jwt
from django.contrib.auth import authenticate
from rest_framework import status
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view


from django.http.response import HttpResponse, JsonResponse
from rest_framework import viewsets

from mediaide import settings
from mediaide_core.confirmation import account_activation_token
from mediaide_core.models import CustomUser, CountryVisa, MedicalPackages, Facilities, UserEnquiry, ContactUs
from mediaide_core.serializer import CustomUserSerializer, CountryVisaSerializer, MedicalPackagesSerializer, \
    FacilitiesSerializer, UserEnquirySerializer, ContactUsSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

class RegisterUser(APIView):
    """
    Register a new user.
    """
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    queryset = CustomUser.objects.all()

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


#TODO UserName Must Be Unique
def confirm(request,confirmation_code, username):
    user = CustomUser.objects.get(name=username)
    if user and account_activation_token.check_token(user,confirmation_code) and user.date_joined > (
            timezone.now() - datetime.timedelta(days=1)):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class ResendMes(APIView):

    def post(self,request,format=None):
        email = request.data.get('email')
        user = CustomUser.objects.get(email=email)

        if user:
            title = "MediAide account confirmation"
            content = " welcome to Mediaide. below is the account activation link  " \
                      "http://localhost:8000/api/confirm/" + str(
                account_activation_token.make_token(user)) + '/' + user.name+'/'
            user.email_user(title,content, 'no-reply@mediaide.com')
            return Response(status=status.HTTP_200_OK)


def forget_password(request):
    email = request.data.get('email',None)
    user_object = CustomUser.objects.filter(email=email)

    if user_object.exists():
        user_object = user_object[0]

        title = " MediAide Password Reset Link "
        content = "below is the password reset link " \
                  "http://localhost:8000/api/confirm/" + str(
            account_activation_token.make_token(user_object))+'/'+user_object.id

        user_object.email_user(title, content, 'no-reply@mediaide.com')


def reset_password(request):
    token = request.data.get('token',None)
    id = request.data.get('id',None)
    password = request.data.get('password', None)
    confirm_password = request.data.get('confirm_password', None)
    user = CustomUser.objects.get(id=id)

    if confirm_password!=password:
        raise serializers.ValidationError(
            "The passwords have to be the same"
        )

    if user and account_activation_token.check_token(user,token):
        user.set_password(password)
        user.save()
        return HttpResponse('password change')


class CustomUserView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class UserEnquiryView(viewsets.ModelViewSet):
    queryset = UserEnquiry.objects.all()
    serializer_class = UserEnquirySerializer


class ContactUsView(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer



class CountryVisaView(viewsets.ModelViewSet):
    queryset = CountryVisa.objects.all()
    serializer_class = CountryVisaSerializer


class MedicalPackagesView(viewsets.ModelViewSet):
    queryset = MedicalPackages.objects.all()
    serializer_class = MedicalPackagesSerializer


class FacilitiesView(viewsets.ModelViewSet):
    queryset = Facilities.objects.all()
    serializer_class = FacilitiesSerializer


class EstimateCost(APIView):

    def post(self,request):
        email = request.data.get('email')
        user = CustomUser.objects.get(email=email)

@api_view(['POST'])
def user_login( request):

    email = request.data.get('email',)
    password = request.data.get('password',)

    if not email and not password:
        pass

    user = authenticate(email=email, password=password)
    if user:
        encoded_token = jwt.encode({'user_id': user.id}, settings.SECRET_KEY, algorithm =settings.JWT_ALGORITHM)
        response_data = CustomUserSerializer().to_representation(user)
        response_data.update({'token':encoded_token})
        return Response(dict(response_data),status=status.HTTP_200_OK)
    else:
        raise serializers.ValidationError('incorrect email or password')
