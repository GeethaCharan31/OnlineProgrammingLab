from django.contrib import admin

# Register your models here.

from .models import Room,Question


admin.site.register(Room)
admin.site.register(Question)