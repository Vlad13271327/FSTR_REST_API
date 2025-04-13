# Generated by Django 5.2 on 2025-04-07 19:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('height', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winter', models.CharField(blank=True, max_length=50)),
                ('summer', models.CharField(blank=True, max_length=50)),
                ('autumn', models.CharField(blank=True, max_length=50)),
                ('spring', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PerevalArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_parent', models.BigIntegerField()),
                ('title', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SprActivitiesType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=20)),
                ('fam', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('otc', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PerevalAdded',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('beauty_title', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('other_titles', models.CharField(blank=True, max_length=255)),
                ('connect', models.CharField(blank=True, max_length=255)),
                ('add_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('new', 'New'), ('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='new', max_length=10)),
                ('coords', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pereval_app.coords')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pereval_app.level')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pereval_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='PerevalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
                ('title', models.CharField(max_length=100)),
                ('pereval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='pereval_app.perevaladded')),
            ],
        ),
    ]
