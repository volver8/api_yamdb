from rest_framework import serializers
from rest_framework.validators import ValidationError

from .constants import EMAIL_LENGTH, USERNAME_LENGTH, ROLES
from .models import User
from .validators import validate_username


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_LENGTH,
        validators=[validate_username]
    )
    email = serializers.EmailField(
        max_length=EMAIL_LEHGTH
    )

    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=USERNAME_LENGTH,
        validators=[validate_username,
                    UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        max_length=EMAIL_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = '__all__'

    def validate_role(self, value):
        if value not in ROLES:
            raise ValidationError(
                'Нет такой роли.'
            )
        return value

class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_LENGTH,
        validators=[validate_username]
    )
    confirmation_code = serializers.CharField()