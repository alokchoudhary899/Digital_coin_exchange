from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    amount = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
