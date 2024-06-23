# school_management/core/serializers.py

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import SiteAdmin, SchoolAdmin, Teacher, Parent, Student, User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


def clean_input(value):
    if not value:
        return value
    cleaned_value = re.sub(r'\s+', '', value.lower())
    if cleaned_value.startswith("+261"):
        cleaned_value = "0" + cleaned_value[4:]
    return cleaned_value


class AuthLoginSerializer(TokenObtainPairSerializer):
    username_field = 'username'

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        # Le nettoyage sera fait avant d'arriver ici
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            if not user:
                raise serializers.ValidationError('Impossible de se connecter avec les identifiants fournis.')

            attrs['user'] = user
        else:
            raise serializers.ValidationError('Le nom d\'utilisateur et le mot de passe sont requis.')

        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['user_type'] = self.user.get_user_type()
        try:
            data['role'] = self.user.role
        except AttributeError:
            pass
        if self.user.email:
            data['email'] = self.user.email
        if self.user.phone_number:
            data['phone_number'] = self.user.phone_number
        if self.user.student_id:
            data['student_id'] = self.user.student_id

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_type'] = user.get_user_type()
        return token


class UserProfileSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'student_id', 'user_type')

    def get_user_type(self, obj):
        return obj.get_user_type()


class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    profile_picture = serializers.ImageField(write_only=True, required=False)
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'phone_number', 'student_id', 'first_name', 'last_name', 'password',
                  'confirm_password', 'profile_picture', 'profile_picture_url',
                  'is_staff')

    def get_profile_picture_url(self, user):
        request = self.context.get('request')
        if user.profile_picture and hasattr(request, 'build_absolute_uri'):
            return request.build_absolute_uri(user.profile_picture.url)
        return None

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Adresse email invalide.")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cette adresse email est déjà utilisée.")
        return value

    def validate_phone_number(self, value):
        cleaned_number = clean_input(value)
        if not re.match(r'^(\+261\d{9}|03\d{8})$', cleaned_number):
            raise serializers.ValidationError(
                "Le numéro de téléphone doit commencer par '+261' suivi de 9 chiffres, ou par '03' suivi de 8 chiffres."
            )
        if User.objects.filter(phone_number=cleaned_number).exists():
            raise serializers.ValidationError("Ce numéro de téléphone est déjà utilisé.")
        return cleaned_number

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Le mot de passe doit contenir au moins une majuscule.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Le mot de passe doit contenir au moins une minuscule.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Le mot de passe doit contenir au moins un chiffre.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Le mot de passe doit contenir au moins un caractère spécial.")
        return value

    def validate_profile_picture(self, value):
        if value:
            if value.size > 5 * 1024 * 1024:  # 5 MB
                raise serializers.ValidationError("L'image ne doit pas dépasser 5 MB.")
            if value.content_type not in ['image/jpeg', 'image/png']:
                raise serializers.ValidationError("Seuls les formats JPEG et PNG sont acceptés.")
        return value

    def validate(self, data):
        if 'password' in data and 'confirm_password' in data:
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)

        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])

        if 'phone_number' in validated_data:
            validated_data['phone_number'] = clean_input(validated_data['phone_number'])

        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('confirm_password', None)

        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))

        if 'phone_number' in validated_data:
            validated_data['phone_number'] = clean_input(validated_data['phone_number'])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def partial_update(self, instance, validated_data):
        return self.update(instance, validated_data)


class SiteAdminSerializer(BaseUserSerializer):
    """
    Serializer pour le modèle SiteAdmin.
    """

    class Meta:
        model = SiteAdmin
        fields = '__all__'


class SchoolAdminSerializer(BaseUserSerializer):
    """
    Serializer pour le modèle SchoolAdmin.
    """

    class Meta:
        model = SchoolAdmin
        fields = '__all__'


class TeacherSerializer(BaseUserSerializer):
    """
    Serializer pour le modèle Teacher.
    """

    class Meta:
        model = Teacher
        fields = '__all__'


class ParentSerializer(BaseUserSerializer):
    """
    Serializer pour le modèle Parent.
    """

    class Meta:
        model = Parent
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Student.
    """

    class Meta:
        model = Student
        fields = '__all__'
