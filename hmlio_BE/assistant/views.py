from rest_framework import generics, filters

from .models import Goal, Instruction
from .serializers import GoalSerializer, InstructionSerializer
# from .tasks import send_goal_confirmation_email


class GoalDetailApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    # permission_classes = [IsAuthenticated]


class GoalListCreateApi(generics.ListCreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        goal = serializer.save()
        # send_goal_confirmation_email.delay(goal.id, self.request.user.email)


class InstructionListApi(generics.ListAPIView):
    serializer_class = InstructionSerializer
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Instruction.objects.select_related("goal")
        goal_id = self.request.query_params.get("goal_id")
        if goal_id:
            queryset = queryset.filter(goal_id=goal_id)
        return queryset
