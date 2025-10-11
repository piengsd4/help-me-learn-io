from django.urls import path
from . import views

urlpatterns = [
    path(
        "generate_instructions/<int:goal_id>/<str:model>",
        views.generate_instructions,
        name="generate-instructions",
    ),
    path(
        "regenerate_instructions/<int:goal_id>/<str:model>",
        views.regenerate_instructions,
        name="regenerate-instructions",
    ),
]
