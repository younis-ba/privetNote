from django.db import models
import uuid

# Create your models here.
class SelfDestory(models.Model):
    name = models.CharField(max_length=200)
    duration=models.DurationField(blank=True , null=True)
    def __str__(self):
        return self.name


class Note(models.Model):
    web_id=models.CharField(max_length=200)
    message=models.TextField()
    email=models.EmailField(blank=True,null=True)
    key=models.CharField(max_length=250 ,blank=True)
    destory_option=models.ForeignKey(SelfDestory,on_delete=models.CASCADE , null=True,blank=True)
    password=models.CharField(max_length=200,blank=True,null=True)
    confirm_password=models.CharField(max_length=200,blank=True,null=True)
    date_created=models.DateTimeField(auto_now=True)
    is_destroy=models.BooleanField(default=False)
    def __str__(self):
        return self.message
