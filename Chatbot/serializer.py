from rest_framework import serializers
from .models import *

class ChatbotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatbot
        fields = ['id', 'name', 'behavior','user']
        read_only_fields = ['user']

