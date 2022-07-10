from operator import sub
from urllib import response
from django import http
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from .serializers import NoteSerializer,SelfDestorySerializer
from .crypto import AESCipher
import bcrypt
from .models import Note, SelfDestory
import secrets
import datetime
from .tasks import send_feedback_email_task

from django.conf import settings
# Create your views here.

@api_view(['POST','OPTIONS'])
def createmessage(request):
    if request.method == 'POST':
        web_id=str(secrets.token_hex(8))
        key = str(secrets.token_hex(32))
        message=AESCipher(key).encrypt(request.GET.get['message'])
        email=request.data['email']
        destory_option=SelfDestory.objects.get(id=request.data['destory_option'])
        try:
            if request.data['password'] == request.data['confirm_password']:
                password=bcrypt.hashpw(request.data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            else :
                return Response({'message': "The password and confirm password does not mtach"})
            Note.objects.create(web_id=web_id, key=key,message=message,password=password,confirm_password=password,destory_option=destory_option, email=email)
            return Response({"url is ":'http://127.0.0.1:8000/show-message/'+ web_id})
        except:
            Note.objects.create(web_id=web_id, key=key,message=message,destory_option=destory_option, email=email)
            return Response({"url is ":'http://127.0.0.1:8000/show-message/'+ web_id + '/'})
    return Response(status=status.HTTP_400_BAD_REQUEST)        



@api_view(['POST','OPTIONS'])
def showmeesage(request,id):
    
    try:
        snippet=Note.objects.get(web_id=id)
        serializer=NoteSerializer(snippet)
        data_created=serializer.data['date_created']
        email=serializer.data['email']
        destroyid=serializer.data['destory_option']
        duration=SelfDestory.objects.get(id=destroyid)

        if duration.duration == None or datetime.datetime.strptime(data_created ,'%Y-%m-%dT%H:%M:%S.%fZ')+ duration.duration >= datetime.datetime.now():
            if snippet.is_destroy == False:
                if serializer.data['password']:
                    try:
                        if bcrypt.checkpw(request.data['password'].encode('utf-8'),serializer.data['password'].encode('utf-8')):
                            message_text=AESCipher(serializer.data['key']).decrypt(serializer.data['message'])
                            snippet.is_destroy=True
                            snippet.save()
                            subject = ' Your user show your message'
                            message = 'Hi  ,thank you for using privet note app  Your user show your message'
                            send_feedback_email_task.delay(subject,message,email)
                            return Response(message_text)

                        else:
                            return Response('Please put correct password')
                    except:
                        return Response('please enter password to show your message')
                else:
                    message_text=AESCipher(serializer.data['key']).decrypt(serializer.data['message'])
                    snippet.is_destroy=True
                    snippet.save()
                    subject = ' Your user show your message'
                    message = 'Hi  ,thank you for using privet note app  Your user show your message'
                    send_feedback_email_task.delay(subject,message,email)
                    return Response(message_text)
            else :
                return Response({'message ' :  "the message is destroyed"})
        else :
            return Response({'message ' :  "the message is destroyed"})
    except Note.DoesNotExist:
        return Response('object does not exist')

