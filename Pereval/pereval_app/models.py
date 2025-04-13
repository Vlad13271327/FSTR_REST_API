from django.db import models


class User(models.Model):
    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=256)
    first_name = models.CharField(verbose_name='Имя', max_length=256)
    middle_name = models.CharField(verbose_name='Отчество', max_length=256)
    phone = models.CharField(verbose_name='Номер телефона', max_length=11)

    def __str__(self):
        return f'{self.pk} {self.last_name} {self.first_name} {self.middle_name}'


class Coords(models.Model):
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    height = models.IntegerField(verbose_name='Высота над уровнем моря')

    def __str__(self):
        return f'latitude:{self.latitude} longitude:{self.longitude} height:{self.height}'


class PerevalAdded(models.Model):
    NEW, PENDING, ACCEPTED, REJECTED = 'NE', 'PE', 'AC', 'RE'
    STATUS_CHOICES = [
        (NEW, 'new'),
        (PENDING, 'pending'),
        (ACCEPTED, 'accepted'),
        (REJECTED, 'rejected')
    ]
    status = models.CharField(verbose_name='Статус', max_length=2, choices=STATUS_CHOICES, default=NEW)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE)
    beauty_title = models.CharField(verbose_name='Тип местности', max_length=256)
    title = models.CharField(verbose_name='Название', max_length=256)
    other_titles = models.CharField(verbose_name='Другие названия', max_length=256)
    connect = models.TextField(verbose_name='Сопроводительный текст', blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    level_spring = models.CharField(verbose_name='Уровень сложности весной', max_length=5, blank=True)
    level_summer = models.CharField(verbose_name='Уровень сложности летом', max_length=5, blank=True)
    level_autumn = models.CharField(verbose_name='Уровень сложности осенью', max_length=5, blank=True)
    level_winter = models.CharField(verbose_name='Уровень сложности зимой', max_length=5, blank=True)


class PerevalImage(models.Model):
    pereval = models.ForeignKey(
        PerevalAdded,
        on_delete=models.CASCADE,
        related_name='attached_images'  # Уникальное имя для обратной связи
    )
    data = models.ImageField(upload_to='images/')
    title = models.CharField(verbose_name='Примечание',max_length=255)

    def __str__(self):
        return self.title


class PerevalArea(models.Model):
    id_parent = models.BigIntegerField()
    title = models.TextField()

    def __str__(self):
        return self.title


class SprActivitiesType(models.Model):
    title = models.TextField()

    def __str__(self):
        return self.title