from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.crypto import get_random_string
from django.utils import timezone


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, default='User')
    groups = models.ManyToManyField(
        Group, blank=True, related_name='custom_users', through='UserGroup'
    )
    user_permissions = models.ManyToManyField(
        Permission, blank=True, related_name='custom_users', through='UserPermission'
    )
    generate_key = models.CharField(max_length=32, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and not self.generate_key:
            self.generate_key = self.cleaned_data['generate_keey']
        super().save(*args, **kwargs)



    def __str__(self):
        return self.username

class UserGroup(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='user_groups')


class UserPermission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='user_permissions')

    
class UploadedFile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    upload_date = models.DateTimeField() 

    def save(self, *args, **kwargs):
        if not self.id:
            self.upload_date = timezone.now()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.file.name


class UserCredentials(models.Model):
    key_field = models.CharField(max_length=100)
    password_field = models.CharField(max_length=100)    
