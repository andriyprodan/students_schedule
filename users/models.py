from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def create_superuser(self, email, phone=None, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMINISTRATOR = 'administrator', 'Адміністратор'
        TEACHER = 'teacher', 'Вчитель'
        STUDENT = 'student', 'Студент'

    role = models.CharField(
        choices=Role.choices, verbose_name="Роль", max_length=20
    )
    # todo
    photo = models.ImageField(null=True, blank=True, upload_to='uploads/users')
    phone = models.CharField(unique=True, null=True, max_length=20)
    email = models.EmailField(blank=False, unique=True)

    # objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        self.username = self.email
        super(User, self).save(*args, **kwargs)
