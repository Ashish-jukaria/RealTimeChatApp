from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

class Group(models.Model):
    group_name = models.CharField(max_length=15)

    def __str__(self):
        return self.group_name

class Chat(models.Model):
    message = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"Chat: {self.message} (Group: {self.group.group_name})"



