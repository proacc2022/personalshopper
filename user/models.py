from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class User1Profile(models.Model):
    address = models.CharField(blank=True, max_length=300)
    city = models.CharField(blank=True, max_length=40)
    state = models.CharField(blank=True, max_length=50)
    pin_code = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=60)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '


class User2Profile(models.Model):
    phone = models.CharField(blank=True, max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, )

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '


class User3Profile(models.Model):
    ccardnumber = models.CharField(blank=True, max_length=16)
    cexpyear = models.CharField(blank=True, max_length=4)
    cexpmonth = models.CharField(blank=True, max_length=2)
    cnameoncard = models.CharField(blank=True, max_length=100)
    ccvv = models.CharField(blank=True, max_length=3)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '


class User4Profile(models.Model):
    dcardnumber = models.CharField(blank=True, max_length=16)
    dexpyear = models.CharField(blank=True, max_length=4)
    dexpmonth = models.CharField(blank=True, max_length=2)
    dnameoncard = models.CharField(blank=True, max_length=100)
    dcvv = models.CharField(blank=True, max_length=3)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '


class User5Profile(models.Model):
    upiid = models.CharField(blank=True, max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '


class User6Profile(models.Model):
    paytmnumber = models.CharField(blank=True, max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '
