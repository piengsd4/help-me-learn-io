from rest_framework import serializers
from .models import Goal, Instruction


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ["id", "title", "description", "created_at", "updated_at"]


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ["id", "goal", "content", "created_at", "updated_at"]
