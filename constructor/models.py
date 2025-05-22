from datetime import timezone

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

sample_states = (
    ('open', 'Опубликована'),
    ('close', 'Закрыта'),
    ('delete', 'Удалена'),
    ('temp', 'Шаблон')
)

class Sample(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.TextField()
    name = models.CharField()
    state = models.CharField(choices=sample_states)
    date_create = models.DateTimeField()
    date_update = models.DateTimeField(null=True)
    image = models.ImageField(upload_to='media/images/', null=True)

roles = (
    ('redactor', 'Редактор'),
)

class UserManager(BaseUserManager):
    def create_user(self, password=None, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)  # автоматически хэширует
        user.save(using=self._db)
        return user

    def create_superuser(self, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(password=password, **extra_fields)

class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(choices=roles)
    first_name = models.CharField(null=True)
    second_name = models.CharField(null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.second_name}'

relations_choise = {
    ('Создатель', 'creator')
}

class SampleUser(models.Model):
    id = models.AutoField(primary_key=True)
    relation = models.CharField(choices=relations_choise)

    user_id = models.ForeignKey('User', models.DO_NOTHING)
    sample = models.ForeignKey('Sample', models.DO_NOTHING)

