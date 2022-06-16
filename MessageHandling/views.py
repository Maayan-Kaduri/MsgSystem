
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from MessageHandling.models import Message
from MessageHandling.serializers import MessageSerializer



class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        emails = [user.email for user in User.objects.all()]
        return Response(emails)



class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })




@api_view(['GET'])
def allMessageApi(request):
    curr_user_id = Token.objects.get(key=request.auth.key).user_id
    if request.method == 'GET':
        messages = Message.objects.filter(receiver_email_id=curr_user_id)
        message_serializer = MessageSerializer(messages, many=True)
        return JsonResponse({"messages" : message_serializer.data}, safe = False)
    


@api_view(['GET'])
def unreadMessageApi(request):
    curr_user_id = Token.objects.get(key=request.auth.key).user_id
    if request.method == 'GET':
        messages = Message.objects.filter(receiver_email_id=curr_user_id,read=False)
        message_serializer = MessageSerializer(messages, many=True)
        return JsonResponse({"messages" : message_serializer.data}, safe = False)


@api_view(['POST'])    
def writeMessageApi(request):
    if request.method == 'POST':
        message_data = JSONParser().parse(request)
        message_serializer = MessageSerializer(data=message_data)
        if message_serializer.is_valid():
            message_serializer.save() 
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False) 




@api_view(['PUT'])
def readMsgApi(request, id):
    try:
        message = Message.objects.get(message_id=id)
    except Message.DoesNotExist:
        return JsonResponse("Message doesn't exist!", safe=False) 
    curr_user_id = Token.objects.get(key=request.auth.key).user_id
    if request.method == 'PUT':
        message_serializer = MessageSerializer(message, data=request.data)
        if message.receiver_email_id==curr_user_id:
            if message_serializer.is_valid():
                message_serializer.save() 
                return Response(message_serializer.data)
        return JsonResponse("Failed to read message!", safe=False) 


@api_view(['DELETE'])
def deleteMsgApi(request, id):
    try:
        message = Message.objects.get(message_id=id)
    except Message.DoesNotExist:
        return JsonResponse("Message doesn't exist!", safe=False) 
    curr_user_id = Token.objects.get(key=request.auth.key).user_id
    if request.method == 'DELETE':
        if (message.receiver_email_id==curr_user_id or message.sender_email_id==curr_user_id):
            message.delete()
            return JsonResponse("The message was deleted successfully!", safe = False)
        else:
            return JsonResponse("You aren't the sender or the receiever of this message! Therefore you can't delete it", safe=False) 


