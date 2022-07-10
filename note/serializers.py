from rest_framework import serializers
from .models import *


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class SelfDestorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfDestory
        fields = '__all__'

