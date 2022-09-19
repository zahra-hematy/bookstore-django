import email
from django.contrib.auth import get_user_model
from django.contrib.auth import backends
from sympy import Q
from django.db.models import Q

User = get_user_model

class EmailUsernameBackend(backends.ModelBackend):

    def authenticate(self, request, username = None, password = None, **kwargs: Any):
        try:
            q = Q(username__iexact=username)|Q(email_iexact=username)
            user = User.objects.get(q)

        except User.DoesNotExist:
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return super().authenticate(request, username = None, password = None, **kwargs: Any)