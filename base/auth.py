from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class MyAuth(ModelBackend):
    """
    Authenticate by email address instead of username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        if not username or password is None:
            return None
        try:
            user = user_model._default_manager.get(email__iexact=username)
        except user_model.DoesNotExist:
            # Run the password hasher once anyway, to mitigate a timing
            # attack telling apart existing and non-existing emails.
            user_model().set_password(password)
            return None
        except user_model.MultipleObjectsReturned:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
