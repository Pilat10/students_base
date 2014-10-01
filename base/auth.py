from django.conf import settings
from django.contrib.auth import get_user_model


class MyAuth(object):
    """

    """

    def authenticate(self, username, password):
        try:
            user = get_user_model().objects.get(email=username)
        except get_user_model().DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None


