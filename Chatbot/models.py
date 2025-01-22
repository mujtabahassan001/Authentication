from django.db import models
from Auth.models import Auth

class Chatbot(models.Model):
    user= models.ForeignKey(Auth, on_delete=models.CASCADE, related_name='chatbot')
    name= models.CharField(max_length=100)
    behavior= models.CharField(max_length=100)


    def __str__(self):
        return self.name
