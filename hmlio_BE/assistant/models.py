from datetime import date
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Goal(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # full_clean() now also checks constraints since Django 4.1
    # class Meta:
    #     constraints = [
    #         models.CheckConstraint
    #     ]

    # This is for validation logic -> this is to ensure quality data in our DB
    # For this to be used, in the service logic before a save(), a full_clean() needs to be called
    # More complex validation logic can be moved to service logic
    def clean(self):
        if self.created_at > timezone.now:
            raise ValidationError(
                "Goal cannot be created in the future. Stick with past and present people."
            )

    def __str__(self):
        return self.title

    # If logic is more complex and if we need to span multiple relations or fetch additional data,
    # instead of @property, we should rather implement something else (service, selector, utility)
    # Also, a property does not have an argument. If there is an argument, it becomes a method.
    @property
    def has_been_updated(self) -> bool:
        return self.updated_at > self.created_at

    # This is a method
    def is_created_within(self, start: date, end: date) -> bool:
        return start <= self.created_at <= end


class Instruction(BaseModel):
    goal = models.ForeignKey(
        Goal, on_delete=models.CASCADE, related_name="instructions"
    )
    content = models.JSONField()

    # This is for validation logic -> this is to ensure quality data in our DB
    def clean(self):
        pass

    def __str__(self):
        return f"Instructions for {self.goal}"
