# core/mixins.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser


class ProfilePictureMixin:
    parser_classes = [MultiPartParser, FormParser]

    @action(methods=['put', 'patch'], detail=True, parser_classes=[MultiPartParser, FormParser])
    def upload_profile_picture(self, request, pk=None):
        instance = self.get_object()
        if 'profile_picture' in request.data:
            instance.profile_picture = request.data['profile_picture']
            instance.save()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordMixin:
    password_serializer_class = None

    @action(methods=['put', 'patch'], detail=True)
    def change_password(self, request, pk=None):
        instance = self.get_object()
        serializer = self.password_serializer_class(data=request.data)
        if serializer.is_valid():
            password = request.data.get('password')
            confirm_password = request.data.get('confirm_password')
            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()
                return Response({'status': 'password set'})
            else:
                return Response({'status': 'password mismatch'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
