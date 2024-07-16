from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .constants import EMAIL_LEHGTH, MAX_LENGTH
from .models import User
from .validators import validate_username


class UsernameValidators(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH,
        validators=[UnicodeUsernameValidator(), validate_username]
    )


class SignUpSerializer(UsernameValidators):
    email = serializers.EmailField(
        max_length=EMAIL_LEHGTH
    )

    def validate(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        if User.objects.filter(
            email=email
        ).exclude(
            username=username
        ):
            raise serializers.ValidationError(
                'Почта с таким именем уже существует.'
            )
        if User.objects.filter(
            username=username
        ).exclude(
            email=email
        ):
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует.')
        return validated_data


class TokenSerializer(UsernameValidators):
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
