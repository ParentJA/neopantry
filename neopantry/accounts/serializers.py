# Django imports.
from django.contrib.auth import get_user_model

# Third-party imports.
from rest_framework import serializers

__author__ = 'Jason Parent'


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords must match.')
        return data

    def create(self, validated_data):
        password, _ = validated_data.pop('password1'), validated_data.pop('password2')
        user = self.Meta.model.objects.create_user(**{'password': password, **validated_data})
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'photo', 'date_of_birth', 'phone_number',
            'password1', 'password2'
        )
