from rest_framework import serializers
from .models import PerevalAdded, User, Coords, PerevalImage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'


class PerevalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalImage
        fields = ['data', 'title']


class PerevalAddedSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    images = PerevalImageSerializer(many=True)  # Добавляем вложенные изображения

    class Meta:
        model = PerevalAdded
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        images_data = validated_data.pop('images', [])

        # Создаем пользователя
        user, _ = User.objects.get_or_create(**user_data)

        # Создаем координаты
        coords, _ = Coords.objects.get_or_create(**coords_data)

        # Создаем объект PerevalAdded
        pereval = PerevalAdded.objects.create(user=user, coords=coords, **validated_data)

        # Добавляем изображения
        for image_data in images_data:
            PerevalImage.objects.create(pereval=pereval, **image_data)

        return pereval



