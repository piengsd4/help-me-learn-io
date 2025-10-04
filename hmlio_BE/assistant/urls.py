from django.urls import path
from . import views

urlpatterns = [
    path("create-goal/", views.GoalCreate.as_view(), name="create-new-goal"),
    path("update-goal/<int:pk>/", views.GoalUpdate.as_view(), name="update-existing-goal"),
    path("delete-goal/<int:pk>/", views.GoalDelete.as_view(), name="delete-existing-goal"),
]