from django.contrib.auth import get_user_model
from djoser.serializers import (
    UserCreateSerializer as DjoserUserCreateSerializer
)

User = get_user_model()

class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        model = User
        fields = DjoserUserCreateSerializer.Meta.fields + (
            "id_no",
            "security_question",
            "security_answer",
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    