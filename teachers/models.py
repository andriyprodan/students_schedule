from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TeacherQuerySet(models.QuerySet):
    def by_active_role(self):
        return self.select_related('user').filter(user__role=User.Role.TEACHER)


# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher')
    objects = TeacherQuerySet.as_manager()
