from django.contrib.auth.models import User
from rest_framework import serializers
from MessageHandling.models import Message

from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first name', 'last name']
        
        def __str__(self):
            return self.email



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ( 'message_id', 'sender_email','receiver_email', 'message_content', 'creation_date', 'subject', 'read')





       
