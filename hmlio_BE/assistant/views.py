from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Goal
from .serializers import GoalSerializer
from django.db import models

class BaseGoalView:
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

class GoalCreate(BaseGoalView, generics.CreateAPIView):
    # This has POST method
    pass
    
class GoalUpdate(BaseGoalView, generics.UpdateAPIView):
    # This has PUT and PATCH method
    pass

class GoalDelete(BaseGoalView, generics.DestroyAPIView):
    # This has DELETE method
    pass