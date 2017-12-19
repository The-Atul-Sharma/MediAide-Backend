import datetime
from django.utils import timezone

from django.http.response import HttpResponse

from mediaide_core.confirmation import account_activation_token
from mediaide_core.models import CustomUser
from mediaide_core.serializer import CustomUserSerializer
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


def confirm(request,confirmation_code, username):
    user = CustomUser.objects.get(full_name=username)
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
                account_activation_token.make_token(user)) + '/' + user.full_name+'/'
            user.email_user(title,content, 'no-reply@mediaide.com')
            return Response(status=status.HTTP_200_OK)
