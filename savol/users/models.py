import uuid
import random
from django.db import models
from shared.models import BaseModel
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    verified = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
    
    def create_verify_code(self):
        code = "".join([str(random.randint(0, 10000) % 10) for _ in range(5)])
        EmailConfirmation.objects.create(
            user_id=self.id,
            code=code
        )
        return code


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(upload_to='profile-images/')
    bio = models.CharField(max_length=350, default="")

    def __str__(self):
        return f"{self.user.username}'s Profile"


class EmailConfirmation(BaseModel):
    code = models.CharField(max_length=4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verify')
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__())
    
    def save(self, *args, **kwargs):
        self.expiration_time = timezone.now() + timedelta(minutes=5)
        super(EmailConfirmation, self).save(*args, **kwargs)