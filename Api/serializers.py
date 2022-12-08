from rest_framework import serializers
from .models import CustomUser, Artist, Media, Favorite, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(password)
        if user.is_artist and not Artist.objects.filter(user_id=user.id).exists():
            Artist.objects.create(user_id=user.id)
        user.save()
        return user
