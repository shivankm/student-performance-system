"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers

from core.models import Student, StudentSubject, Subject


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)
    
    
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the CustomUser auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the student."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']

class StudentSubjectSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    
    class Meta:
        model = StudentSubject
        fields = ['subject', 'marks']

class StudentSerializer(serializers.ModelSerializer):
    subjects = StudentSubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'subjects']
    