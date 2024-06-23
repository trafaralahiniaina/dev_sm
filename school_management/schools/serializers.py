# schools/serializers.py

import os
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from .models import School, Grade, Section, ClassRoom


class SchoolSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = '__all__'  # This implicitly includes 'sigle' and 'slogan'
        read_only_fields = ['created_at', 'updated_at']

    def get_logo_url(self, obj):
        request = self.context.get('request')
        if obj.logo and request:
            return request.build_absolute_uri(obj.logo.url)
        return None

    def validate_logo(self, value):
        if value:
            # Vérifier l'extension du fichier
            ext = os.path.splitext(value.name)[1]
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg']
            if not ext.lower() in valid_extensions:
                raise serializers.ValidationError('Format de fichier non supporté. Utilisez JPG, JPEG, PNG, GIF ou SVG.')

            # Vérifier la taille du fichier (par exemple, limite à 5 Mo)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError('La taille du fichier ne doit pas dépasser 5 MB.')

            # Ne pas redimensionner les SVG
            if ext.lower() != '.svg':
                # Redimensionner l'image si nécessaire
                img = Image.open(value)
                if img.height > 400 or img.width > 400:
                    img.thumbnail((400, 400))

                    # Convertir l'image en JPEG
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")

                    # Sauvegarder l'image redimensionnée
                    output = BytesIO()
                    img.save(output, format='JPEG', quality=85)
                    output.seek(0)

                    # Créer un nouveau fichier InMemoryUploadedFile
                    value = InMemoryUploadedFile(output, 'ImageField',
                                                 f"{os.path.splitext(value.name)[0]}.jpg",
                                                 'image/jpeg',
                                                 output.getbuffer().nbytes,
                                                 None)

        return value


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('id', 'name', 'subjects', 'school')

    def create(self, validated_data):
        if 'name' in validated_data and isinstance(validated_data['name'], list):
            grades = []
            for grade_name in validated_data['name']:
                grade = Grade.objects.create(name=grade_name, school_id=validated_data['school'])
                grades.append(grade)
            return grades
        else:
            return Grade.objects.create(**validated_data)


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'name', 'grade', 'academic_year')

    def create(self, validated_data):
        if 'name' in validated_data and isinstance(validated_data['name'], list):
            sections = []
            for section_name in validated_data['name']:
                section = Section.objects.create(name=section_name, grade_id=validated_data['grade'],
                                                 academic_year=validated_data['academic_year'])
                sections.append(section)
            return sections
        else:
            return Section.objects.create(**validated_data)


class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom

        fields = ('id', 'name', 'section', 'school')

    def create(self, validated_data):
        if 'name' in validated_data and isinstance(validated_data['name'], list):
            classrooms = []
            for classroom_name in validated_data['name']:
                classroom = ClassRoom.objects.create(name=classroom_name, section_id=validated_data['section'],
                                                     school_id=validated_data['school'])
                classrooms.append(classroom)
            return classrooms
        else:
            return ClassRoom.objects.create(**validated_data)
