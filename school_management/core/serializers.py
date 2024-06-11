# core/serializers.py


from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User, SiteAdmin, SchoolAdmin, Teacher, Parent, Student
from schools.models import School, Section, Grade
from academics.models import Subject
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# Token Serializer with additional user info
class TokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add additional user-specific information
        user_data = {
            'user_id': self.user.id,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'phone_number': getattr(self.user, 'phone_number', None),
            'student_id': getattr(self.user, 'student_id', None),
            'user_type': 'unknown'
        }

        if isinstance(self.user, SiteAdmin):
            user_data['user_type'] = 'site_admin'
        elif isinstance(self.user, SchoolAdmin):
            user_data['user_type'] = 'school_admin'
            user_data['role'] = self.user.get_role_display()
        elif isinstance(self.user, Teacher):
            user_data['user_type'] = 'teacher'
        elif isinstance(self.user, Parent):
            user_data['user_type'] = 'parent'
        elif isinstance(self.user, Student):
            user_data['user_type'] = 'student'

        data.update(user_data)
        return data


# Base User Serializer for common fields
class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    profile_picture = serializers.ImageField(write_only=True, required=False)
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password',
                  'confirm_password', 'profile_picture', 'profile_picture_url',
                  'is_staff')

    def get_profile_picture_url(self, user):
        request = self.context.get('request')
        if user.profile_picture and hasattr(request, 'build_absolute_uri'):
            return request.build_absolute_uri(user.profile_picture.url)
        return None

    def validate(self, data):
        if data.get('password') or data.get('confirm_password'):
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password', None)
        if password:
            validated_data['password'] = make_password(password)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


# Serializer for SiteAdmin users
class SiteAdminSerializer(BaseUserSerializer):
    role = serializers.CharField(source='get_role_display', read_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = SiteAdmin
        fields = BaseUserSerializer.Meta.fields + ('role',)


# Serializer for SchoolAdmin users
class SchoolAdminSerializer(BaseUserSerializer):
    role = serializers.ChoiceField(choices=SchoolAdmin.role.field.choices, required=True)
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all(), required=True)

    class Meta(BaseUserSerializer.Meta):
        model = SchoolAdmin
        fields = BaseUserSerializer.Meta.fields + ('role', 'school')


# Serializer for Teacher users
class TeacherSerializer(BaseUserSerializer):
    teacher_schools = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all(), many=True, required=True)
    teacher_subjects = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), many=True, required=True)
    phone_number = serializers.CharField(required=True)

    class Meta(BaseUserSerializer.Meta):
        model = Teacher
        fields = BaseUserSerializer.Meta.fields + ('teacher_schools', 'teacher_subjects', 'phone_number')

    def validate_phone_number(self, value):
        if Teacher.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Ce numéro de téléphone existe déjà pour un autre enseignant.")
        return value


# Serializer for Parent users
class ParentSerializer(BaseUserSerializer):
    phone_number = serializers.CharField(required=True)
    parent_children_schools = serializers.PrimaryKeyRelatedField(queryset=School.objects.all(), many=True,
                                                                 required=True)
    address = serializers.CharField(required=False)
    status = serializers.CharField(source='get_status_display', read_only=True)
    mother_first_name = serializers.CharField(max_length=30, default='NC')
    mother_last_name = serializers.CharField(max_length=30, default='NC')
    mother_job = serializers.CharField(max_length=50, default='NC')
    father_first_name = serializers.CharField(max_length=30, default='NC')
    father_last_name = serializers.CharField(max_length=30, default='NC')
    father_job = serializers.CharField(max_length=50, default='NC')
    tutor_first_name = serializers.CharField(max_length=30, default='NC')
    tutor_last_name = serializers.CharField(max_length=30, default='NC')
    tutor_job = serializers.CharField(max_length=50, default='NC')

    class Meta:
        model = Parent
        fields = BaseUserSerializer.Meta.fields + (
            'phone_number', 'parent_children_schools', 'address', 'status',
            'mother_first_name', 'mother_last_name', 'mother_job',
            'father_first_name', 'father_last_name', 'father_job',
            'tutor_first_name', 'tutor_last_name', 'tutor_job'
        )

    def validate_phone_number(self, value):
        if Parent.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Ce numéro de téléphone existe déjà pour un autre parent.")
        return value


# Serializer for Student users
class StudentSerializer(BaseUserSerializer):
    student_id = serializers.CharField(required=True)
    grade_level = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all(), required=True)
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all(), required=True)
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all(), required=True)
    student_parent = serializers.PrimaryKeyRelatedField(queryset=Parent.objects.all(), required=False, allow_null=True)
    address = serializers.CharField(required=True)

    class Meta:
        model = Student
        fields = BaseUserSerializer.Meta.fields + (
            'student_id', 'grade_level', 'section', 'school', 'student_parent', 'address'
        )

    def validate_student_id(self, value):
        if Student.objects.filter(student_id=value).exists():
            raise serializers.ValidationError("L'ID étudiant existe déjà.")
        return value


# Serializer for changing a student's password
class StudentPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        instance.set_password(password)
        instance.save()
        return instance


# Combined User Serializer that includes all user types
class UserSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'profile_picture_url', 'is_staff', 'is_active')

    def get_profile_picture_url(self, user):
        request = self.context.get('request')
        if user.profile_picture and hasattr(request, 'build_absolute_uri'):
            return request.build_absolute_uri(user.profile_picture.url)
        return None
