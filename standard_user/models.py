from django.db import models
from accounts.models import CustomUser
from power_user.models import PowerUser


# Create your models here.
class StandardUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='standard_user')

    supervisor = models.ForeignKey(PowerUser, on_delete=models.CASCADE, related_name='supervisor_power_user')


    contact_no = models.CharField(max_length=11)


    def __str__(self):
        return f'{self.user.username} (standard user)'


