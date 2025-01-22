from rest_framework import viewsets
from Chatbot.serializer import ChatbotSerializer
from Chatbot.models import Chatbot
from Auth.utils import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class ChatbotViewSet(viewsets.ViewSet):
    serializer_class=ChatbotSerializer
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def list(self, request):
        chatbot=Chatbot.objects.filter(user=self.request.user)
        serializer=self.serializer_class(chatbot, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        chatbot=Chatbot.objects.get(id=pk)
        serializer=self.serializer_class(chatbot)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        chatbot=Chatbot.objects.get(id=pk)
        serializer=self.serializer_class(instance=chatbot, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        chatbot=Chatbot.objects.get(id=pk)
        chatbot.delete()
        return Response("Chatbot deleted successfully")