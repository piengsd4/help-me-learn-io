import json
import asyncio
from assistant.models import Goal, Instruction
from assistant.serializers import InstructionSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ollama import ChatResponse, AsyncClient


async def generate_with_llm(goal: Goal, model: str) -> str:
    print(f"Starting LLM generation for goal: {goal.description} with model: {model}")

    if model == "test":
        print("Returning mock instructions for testing")
        return {
            "Step 1": "Do A",
            "Step 2": "Watch B",
            "Step 3": "Write C",
            "Step 4": "Exercise",
            "Step 5": "Sleep more",
        }

    # LLM Prompt
    messages: list[dict] = [
        {
            "role": "system",
            "content": """
                       You are a learning assistant. Generate clear, actionable learning instructions based on the user's goal.
                       Always return your response in JSON format. You response will only include purely the JSON.
                       Example format: { "Step 1": "Do A", "Step 2": "Watch B", "Step 3": "Write C" }
                       """,
        },
        {
            "role": "user",
            "content": f"Goal: {goal.description}\n\nGenerate 5-10 step-by-step learning instructions for this goal in JSON format.",
        },
    ]

    # Request to LLM
    print("Sending request to Ollama...")
    response: ChatResponse = await AsyncClient().chat(model=model, messages=messages)
    print(f"Received response: {response.message.content}")

    # Parse the JSON string returned from LLM
    instructions = json.loads(response.message.content)

    return instructions


@api_view(["POST"])
def generate_instructions(_request, goal_id: int, model: str) -> Response:
    goal = Goal.objects.filter(id=goal_id).first()
    if not goal:
        return Response({"error": "Goal not found"}, status=status.HTTP_404_NOT_FOUND)

    result = asyncio.run(generate_with_llm(goal=goal, model=model))

    # Replace any existing instructions for this goal so the client only sees the latest set
    Instruction.objects.filter(goal_id=goal_id).delete()

    # Create instruction with the LLM response
    serializer = InstructionSerializer(data={"goal": goal_id, "content": result})
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"generated_instructions": result}, status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def regenerate_instructions(_request, goal_id: int, model: str) -> Response:
    goal = Goal.objects.filter(id=goal_id).first()
    if not goal:
        return Response({"error": "Goal not found"}, status=status.HTTP_404_NOT_FOUND)

    result = asyncio.run(generate_with_llm(goal=goal, model=model))

    # Delete old instructions for this goal and create new ones
    Instruction.objects.filter(goal_id=goal_id).delete()

    serializer = InstructionSerializer(data={"goal": goal_id, "content": result})
    if serializer.is_valid():
        serializer.save()
        return Response({"regenerated_instructions": result})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
