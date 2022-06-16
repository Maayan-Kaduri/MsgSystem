from django.contrib import admin

from .models import Message#, User

# Register your models here.

class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'creation_date', 'subject', 'sender_email', 'receiver_email', 'read', 'message_content')
    list_filter = ('creation_date', 'subject', 'sender_email', 'receiver_email', 'read') 
   



admin.site.register(Message, MessageAdmin) #registering the given model with the given admin class
