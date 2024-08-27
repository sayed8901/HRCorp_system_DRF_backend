from django.db import models
from accounts.models import CustomUser


# Create your models here.
class PowerUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='power_user')

    contact_no = models.CharField(max_length=11)


    def __str__(self):
        return f'{self.user.username} (power user)'

