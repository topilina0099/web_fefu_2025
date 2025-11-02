from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class UserProfile(models.Model):
    username = models.CharField(max_length=50, unique=True, verbose_name='Логин')
    email = models.EmailField(unique=True, verbose_name='Email')
    password = models.CharField(max_length=128, verbose_name='Пароль')

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username
