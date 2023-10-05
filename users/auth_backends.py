from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

UserModel = get_user_model()


class EmailOrPhoneBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if not username:
                raise UserModel.DoesNotExist
            user = UserModel.objects.get(Q(email=username) | Q(phone=username))
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
