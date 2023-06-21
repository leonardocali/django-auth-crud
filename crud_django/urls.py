"""
URL configuration for crud_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tasks import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name='home'),
    path("singup/", views.singup, name='singup'),
    path("task/", views.tasks, name='task'),
    path("logout/", views.outsession, name='logout'),
    path("login/", views.loginUser, name='login'),
    path("create/task", views.create_task, name='create_task'),
    path("task_detail/<int:taskid>/", views.task_detail, name='task_detail'),
    path("complete_task/<int:taskid>/", views.complete_task, name='complete_task'),
    path("delete_task/<int:taskid>/", views.delete_task, name='delete_task'),
    path("list_task_complete/", views.list_completed_task, name='list_task_completed'),
]
