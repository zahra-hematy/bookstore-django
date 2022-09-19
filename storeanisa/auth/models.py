import uuid
from django.db import models
import time
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    def __str__(self) -> str:
        return self.email

    def get_full_name(self) -> str:
        if self.get_short_name():
            return self.get_short_name()
        return self.email

    def get_short_name(self) -> str:
        return self.last_name

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    value = models.CharField(max_length=100)
    creat_date = models.DateTimeField(auto_now=True)
    def generate(self, length=None):
        v = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(time.time())))
        if not length:
            self.value=v
        else:
            self.value=v[:length]
        return self.value