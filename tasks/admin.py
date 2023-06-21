from django.contrib import admin
from .models import Task
# Register your models here.

#Clase para mostrar campos de solo lectura en el admin
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Task, TaskAdmin)