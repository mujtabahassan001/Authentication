from rest_framework.routers import DefaultRouter

from .views import ChatbotViewSet

router = DefaultRouter()
router.register(r'chatbots', ChatbotViewSet, basename='chatbot')

urlpatterns = router.urls