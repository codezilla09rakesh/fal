from rest_framework import serializers
from .models import User
from cities_light.models import Country, Region



class CountrySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    class Meta:
        model = Country
        fields = ['id', 'name', 'code2']


class StateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    class Meta:
        model = Region
        fields = ['id', 'name']


class CreateUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)
    dob = serializers.DateField(required=True)
    # role = serializers.CharField(required=True)
    # profile_picture = serializers.ImageField(required=True)
    country = CountrySerializer()
    state = StateSerializer()
    visitReason = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "gender",
            "dob",
            "profile_picture",
            "country",
            "state",
            "visitReason",
            # "role",
        )
        write_only_fields = ("password",)
        read_only_fields = ("id",)

        depth = 1

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        if not user.is_superuser:
            user.role = 'customer'
        user.is_active = False
        user.save()
        return user

    def validate_username(self, value):
        if User.objects.filter(username=value):
            raise serializers.ValidationError("This field must be unique.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value):
            raise serializers.ValidationError("This field must be unique.")
        return value


class LoginAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")
        extra_kwargs = {
            "username": {
                "required": True,
                "error_messages": {"required": "Please fill username field", },
            },

            "password": {
                "required": True,
                "error_messages": {"required": "Please fill password field", },
            },
        }


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "profile_picture",
            "gender",
            "dob",
            "country",
            "state",
            # "visit_reason",
            # "strip_id"
        )

    read_only_fields = ("id",)


class ReadUserSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    state = StateSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "profile_picture",
            "gender",
            "dob",
            "country",
            "state"
        )
        depth = 1

    read_only_fields = ("id")
