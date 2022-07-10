from django.contrib import admin
from .models import Note , SelfDestory
# Register your models here.

class SelfDestoryAdmin(admin.ModelAdmin):
    list_display = ['name','duration']

class NoteAdmin(admin.ModelAdmin):
    list_display = ['web_id','message','email','key','destory_option','password','confirm_password','date_created']

admin.site.register(SelfDestory,SelfDestoryAdmin)
admin.site.register(Note,NoteAdmin)