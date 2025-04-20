from rest_framework import serializers
from .models import PerevalAdded, User, Coords, PerevalImage


class UserSerializer(serializers.ModelSerializer):
    """
         Сериализатор пользователя.

         Включает:
         - email (уникальный);
         - фамилия, имя, отчество;
         - номер телефона.

         Используется при добавлении и отображении информации о пользователе.
     """
    class Meta:
        model = User
        fields = '__all__'


class CoordsSerializer(serializers.ModelSerializer):
    """
         Сериализатор координат перевала.

         Включает:
         - широту (latitude),
         - долготу (longitude),
         - высоту (height).

         Используется в структуре перевала.
     """
    class Meta:
        model = Coords
        fields = '__all__'


class PerevalImageSerializer(serializers.ModelSerializer):
    """
         Сериализатор изображений перевала.

         Включает:
         - строку изображения (data),
         - подпись к изображению (title).

         Используется для добавления и отображения фото перевала.
     """
    class Meta:
        model = PerevalImage
        fields = ['data', 'title']


class PerevalAddedSerializer(serializers.ModelSerializer):
    """
         Сериализатор для модели PerevalAdded.

         Используется при добавлении, редактировании и выводе информации о перевалах.

         Включает:
         - пользователя (user),
         - координаты (coords),
         - изображения (images),
         - прочие поля модели перевала.
     """
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


    def update(self, instance, validated_data):
        # Обновляем данные Pereval
        instance.status = validated_data.get('status', instance.status)
        instance.beauty_title = validated_data.get('beauty_title', instance.beauty_title)
        instance.title = validated_data.get('title', instance.title)
        instance.other_titles = validated_data.get('other_titles', instance.other_titles)
        instance.connect = validated_data.get('connect', instance.connect)
        instance.level_spring = validated_data.get('level_spring', instance.level_spring)
        instance.level_summer = validated_data.get('level_summer', instance.level_summer)
        instance.level_autumn = validated_data.get('level_autumn', instance.level_autumn)
        instance.level_winter = validated_data.get('level_winter', instance.level_winter)
        instance.save()

        # Обновляем данные Coords
        coords_data = validated_data.get('coords', {})
        coords = instance.coords
        coords.latitude = coords_data.get('latitude', coords.latitude)
        coords.longitude = coords_data.get('longitude', coords.longitude)
        coords.height = coords_data.get('height', coords.height)
        coords.save()

        # Обновляем данные User
        user_data = validated_data.get('user', {})
        user = instance.user
        user.email = user_data.get('email', user.email)
        user.last_name = user_data.get('last_name', user.last_name)
        user.first_name = user_data.get('first_name', user.first_name)
        user.middle_name = user_data.get('middle_name', user.middle_name)
        user.phone = user_data.get('phone', user.phone)
        user.save()

        # Обновляем изображения (если нужно)
        images_data = validated_data.get('attached_images', [])
        instance.attached_images.all().delete()  # Удаляем старые изображения
        for image_data in images_data:
            PerevalImage.objects.create(pereval=instance, **image_data)

        return instance