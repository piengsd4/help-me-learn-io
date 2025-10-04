from django.contrib import admin
from .models import Goal, Instruction

# Register your models here.
admin.site.register([Goal, Instruction])