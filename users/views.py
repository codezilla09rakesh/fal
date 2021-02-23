import uuid
import json
import re
import requests

from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.mixins import Response, status, UpdateModelMixin
from rest_framework.generics import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope

import stripe

from .models import User
from .serializers import (
    CreateUserSerializer,
    LoginAuthSerializer,
    ChangePasswordSerializer,
    UpdateUserSerializer,
    ReadUserSerializer
)

from ThanksFinance import settings


class Register(GenericAPIView):
    permission_classes = []

    serializer_class = CreateUserSerializer

    def post(self, request):
        """
        :param request: username, password, email, first_name, last_name, gender, dob, country, state, visit_reason
        :return: success message: Registered successfully
        """

        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():

            try:
                # Adding user info to stripe
                stripe.api_key = settings.STRIPE_KEY
                r = stripe.Customer.create(
                    address={'country': request.data['country'], 'state': request.data['state']},
                    email=request.data['email'],
                    name=request.data['first_name'] + " " + request.data['last_name'],
                )
                serializer.save()

                # Adding stripe ID to user object
                instance = User.objects.get(email=request.data['email'])
                instance.strip_id = r.get("id")
                instance.save()

                # Creating default plan for user
                # plan_instance = Plans.objects.get(id=settings.DEFAULT_PLAN)
                # subscription_object = Subscriptions(user=instance, plan=plan_instance)
                # subscription_object.save()

                return Response({"message": "Registered successfully"})

            except Exception as e:
                return Response(data={'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors)


class Token(ObtainAuthToken, GenericAPIView):
    permission_classes = []
    serializer_class = LoginAuthSerializer

    def post(self, request, *args, **kwargs):
        """
        :param request: username, password
        :param args:
        :param kwargs:
        :return: user data, token data
        """

        try:
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
            if re.search(regex, request.data["username"]):
                user = User.objects.filter(email=request.data["username"])
                if len(user):
                    username = user[0].username
                    # isVerified = user[0].isVerified
                    scope = user[0].role
                    if user[0].is_active == False:
                        return Response({
                            "message": "Your account has been suspended, please contact customer care service for more information."})
                    # elif isVerified == False:
                    #     return Response({"message": "Email not verified."})
                    user = user[0]
                else:
                    return Response(data={"message": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.get(username=request.data["username"])
                username = request.data["username"]
                # isVerified = user.isVerified
                scope = user.role
                if user.is_active == False:
                    return Response({
                        "message": "Your account has been suspended, please contact customer care service for more information."})
                # elif isVerified == False:
                #     return Response({"message": "Email not verified."})


        except Exception as e:

            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'error': str(e)})

        r = requests.post(settings.URL_TYPE + "/o/token/",
                          data={
                              "grant_type": "password",
                              "username": username,
                              "password": request.data["password"],
                              "scope": scope,
                              "client_id": settings.CLIENT_ID,
                              "client_secret": settings.CLIENT_SECRET,
                          },
                          )

        if r.status_code == 400:
            json_res = {"message": "Bad request or Invalid credentials"}
            return Response(data=json_res, status=r.status_code)
        else:
            res = r.json()

            res['strip_id'] = user.strip_id
            res['fullname'] = user.fullname()
            res['email'] = user.email
            return Response(res)


class ChangePasswordView(UpdateAPIView):
    """ An endpoint for changing password. """
    model = User
    serializer_class = ChangePasswordSerializer
    authentication_classes = [OAuth2Authentication]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        """
        :param request: old_password, new_password
        :param args:
        :param kwargs:
        :return: success message
        """
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(RetrieveAPIView, ListAPIView, UpdateModelMixin):
    serializer_class = UpdateUserSerializer
    authentication_classes = [OAuth2Authentication]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProfileView
        return ReadUserSerializer

    def get_object(self):
        obj = get_object_or_404(User, id=self.request.user.id)
        return obj

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class RefreshToken(APIView):
    permission_classes = []

    def post(self, request):
        """
        :param request: refresh_token
        :return: access_token, refresh_token, scope, validity
        """
        r = requests.post(
            settings.URL_TYPE + "/o/token/",
            data={
                "grant_type": "refresh_token",
                "refresh_token": request.data["refresh_token"],
                "client_id": settings.CLIENT_ID,
                "client_secret": settings.CLIENT_SECRET,
            },
            verify=False,
        )
        if r.status_code == 200:
            return Response(r.json())
        else:
            return Response(r.json(), r.status_code)


@api_view(["POST"])
@permission_classes([AllowAny])
def revoke_token(request):
    """
    :param request: token
    :return: success message
    """

    r = requests.post(
        settings.URL_TYPE + "/o/revoke_token/",
        data={
            "token": request.data["token"],
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
        },
    )
    # If it goes well return success message (would be empty otherwise)
    if r.status_code == requests.codes.ok:
        return Response({"message": "token revoked"}, r.status_code)

    # Return the error if it goes badly
    return Response(r.json(), r.status_code)
