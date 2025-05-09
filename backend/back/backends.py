from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            return None
        try:
            # Try to authenticate using email
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                # If email is not found, try to authenticate using username
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        
        # If the user is found, check the password
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
