from rest_framework import viewsets
from .models import Goal, Instruction
from .serializers import GoalSerializer, InstructionSerializer


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

    # These are straightforward, only post, put, get
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class InstructionViewSet(viewsets.ModelViewSet):
    serializer_class = InstructionSerializer

    def get_queryset(self):
        queryset = Instruction.objects.all()
        goal_id = self.request.query_params.get("goal_id")
        if goal_id:
            queryset = queryset.filter(goal_id=goal_id)
        return queryset

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # The instructions should get updated through the LLM when we refresh
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
