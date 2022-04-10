from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


# Create your models here.


# UserModel
class CustomUser(AbstractUser):
    email = models.EmailField('Email Address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class FolFolRel(models.Model):
    p_folder = models.TextField()

    c_folder = models.CharField(max_length=20)
    c_folder_brief = models.CharField(max_length=50, blank=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return "U:{} / F:{} / F:{}".format(self.user, self.p_folder, self.c_folder)

    def get_c_folder(self):
        return self.c_folder, self.c_folder_brief


class FolTabRel(models.Model):
    p_folder = models.TextField()

    c_table = models.CharField(max_length=20)
    c_table_brief = models.CharField(max_length=50, blank=True)
    is_fav = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return "U:{} / F:{} / T:{}".format(self.user, self.p_folder, self.c_table)

    def get_c_table(self):
        return self.c_table, self.c_table_brief

    def is_table_fav(self):
        return self.is_fav

    def is_table_pinned(self):
        return self.is_pinned
