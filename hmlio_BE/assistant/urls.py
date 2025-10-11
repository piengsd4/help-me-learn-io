from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GoalViewSet, InstructionViewSet

router = DefaultRouter()
router.register(r"goal", GoalViewSet, basename="goal")
router.register(r"instructions", InstructionViewSet, basename="instruction")

urlpatterns = [path("", include(router.urls))]
