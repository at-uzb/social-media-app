# Generated by Django 5.0.3 on 2024-04-13 15:20

import django.core.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('image1', models.ImageField(blank=True, upload_to='post_images', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])])),
                ('image2', models.ImageField(blank=True, upload_to='post_images', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])])),
                ('image3', models.ImageField(blank=True, upload_to='post_images', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png'])])),
                ('caption', models.TextField(validators=[django.core.validators.MaxLengthValidator(2000)])),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'db_table': 'posts',
            },
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]