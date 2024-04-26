from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from allauth.headless.account.views import ChangePasswordView
from api.docs.utils import successful_api_response
from .utils import generate_username
from .models import User
from .permissions import DeleteUserPermission
from .serializers import (
    ListUserSerializer,
    UserDetailsSerializer,
    ProfileSerializer,
    SuggestUsernameSerializer,
    PhoneNumberSerializer,
)
from .pagination import UserCursorPagination


class UsersView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ListUserSerializer
    pagination_class = UserCursorPagination


class ProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class UserDetailsView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, DeleteUserPermission)
    queryset = User.objects.all()
    lookup_field = "username"
    serializer_class = UserDetailsSerializer



class SuggestUsernameView(APIView):
    serializer_class = SuggestUsernameSerializer
    
    @extend_schema(
        responses={
            200: successful_api_response({
                'data': serializers.ListField(child=serializers.CharField())
            }),
        },
    )
    def get(self, request):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        prefix = serializer.validated_data.get('prefix')
        max_suggestions = serializer.validated_data['max_suggestions']
        
        suggested_usernames = []
        for _ in range(max_suggestions):
            if suggested_username := generate_username(prefix):
                suggested_usernames.append(suggested_username)
        
        return Response(suggested_usernames)

class PasswordChangeView(ChangePasswordView):
    http_method_names = ("patch",)

    def patch(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class PhoneNumberView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None

    @extend_schema(
        request=PhoneNumberSerializer,
        responses={
            200: successful_api_response(),
            202: successful_api_response(
                description="Verification code sent to the phone number"
            ),
        },
    )
    def patch(self, request):
        serializer = PhoneNumberSerializer(
            self.request.user,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if "otp" in serializer.validated_data:
            return Response("Phone number updated!")
        return Response(
            "Verification code sent to the phone number!",
            status=status.HTTP_202_ACCEPTED,
        )

    def delete(self, request):
        user = self.request.user
        user.phone_number = None
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
        