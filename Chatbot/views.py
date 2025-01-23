import os
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from Chatbot.serializer import ChatbotSerializer
from Chatbot.models import Chatbot
from Auth.utils import JWTAuthentication
from rest_framework.decorators import action

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing. Please set it in the .env file.")

genai.configure(api_key=GEMINI_API_KEY)


class ChatbotViewSet(viewsets.ViewSet):
    serializer_class = ChatbotSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        chatbots = Chatbot.objects.filter(user=self.request.user)
        serializer = self.serializer_class(chatbots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        if pk is None:
            return Response({"error": "Chatbot ID is missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            chatbot = Chatbot.objects.get(user=self.request.user, id=pk)
        except Chatbot.DoesNotExist:
            return Response({"error": "Chatbot not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(chatbot)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        if pk is None:
            return Response({"error": "Chatbot ID is missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            chatbot = Chatbot.objects.get(user=self.request.user, id=pk)
        except Chatbot.DoesNotExist:
            return Response({"error": "Chatbot not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(instance=chatbot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        if pk is None:
            return Response({"error": "Chatbot ID is missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            chatbot = Chatbot.objects.get(user=self.request.user, id=pk)
            chatbot.delete()
            return Response({"message": "Chatbot deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Chatbot.DoesNotExist:
            return Response({"error": "Chatbot not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['post'], url_path='chat')
    def chat_with_bot(self, request, pk=None):
        try:
            chatbot = Chatbot.objects.get(user=self.request.user, id=pk)
        except Chatbot.DoesNotExist:
            return Response(
                {"error": "Chatbot not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        query = request.data.get('query')
        if not query:
            return Response(
                {"error": "Query is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        prompt = f"""
        You are an AI assistant with the following behavior: {chatbot.behavior}
        
        User Query: {query}
        
        Provide a response that aligns with the specified behavior.
        """
        
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            
            return Response({
                'query': query,
                'response': response.text
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': f'Error generating response: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




