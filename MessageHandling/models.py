from django.db import models
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
from datetime import date

# Create your models here.


User = settings.AUTH_USER_MODEL  # grabing the User model

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender_email = models.ForeignKey( User , on_delete=models.PROTECT, related_name="sender" )
    receiver_email =  models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="receiver")
    message_content = models.TextField()
    creation_date = models.DateField(("Date"), default=date.today)
    subject = models.CharField(max_length=50)
    read = models.BooleanField(default=False)

