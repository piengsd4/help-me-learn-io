from django.urls import path
from . import views

# For ModelViewSet:
# router = DefaultRouter()
# router.register(r"goal", GoalViewSet, basename="goal")
# router.register(r"instructions", InstructionViewSet, basename="instruction")

# urlpatterns = [path("", include(router.urls))]

urlpatterns = [
    path("goal/<int:pk>", views.GoalDetailApi.as_view(), name="goal-detail"),
    path("goal/", views.GoalListCreateApi.as_view(), name="goal-list"),
    path("instruction/", views.InstructionListApi.as_view(), name="instruction-list"),
]
