from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from .forms import TaskForm
from .models import Task

# Create your views here.
def home(request):
    return render(request, 'home.html')

def singup(request):
    if request.method == 'GET':
        print("envio formulario")
        return render(request, 'singup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            print(request.POST['password1']+"--------"+request.POST['password2'])
            try:
                #print("same pass")
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                print(user)
                login(request,user)
                return redirect('task')
            except IntegrityError:
                return render(request, 'singup.html', {
                    'form': UserCreationForm,
                    'error': "Username already exists"
                })
        else:
            return render(request, 'singup.html', {
                'form': UserCreationForm,
                'error': "Password do not match"
            })

@login_required
def tasks(request):
        try:
            tasklist = Task.objects.filter(user=request.user, datecompleted__isnull=True)
            return render(request, 'tasks.html' , {'listask': tasklist})
        except:
            return redirect('home')

@login_required
def outsession(request):
    logout(request)
    return redirect('home')

def loginUser(request):
    if request.method == 'GET':
        return render(request, 'login.html' , {'form': AuthenticationForm})
    else:
        print(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request,user)
            return redirect('create_task')
        else:
            return render(request, 'login.html',{
                'form': AuthenticationForm,
                'error':"User or password wrong"
                })
@login_required        
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {'formtask':TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            newtask = form.save(commit=False)
            newtask.user = request.user
            newtask.save()
            return redirect('task')
        except ValueError:
            return render(request, 'create_task.html', {
                'formtask':TaskForm,
                'error':"Could not execute the task"                                  
                                                        })
@login_required
def task_detail(request,taskid):
    if request.method == 'GET':
        tarea = get_object_or_404(Task,pk=taskid)
        form = TaskForm(instance=tarea)
        return render(request, 'task_detail.html', {'task':tarea,
                                                    'form': form})
    else:
        try:         
            tarea = get_object_or_404(Task, pk=taskid)
            form = TaskForm(request.POST,instance=tarea)
            form.save()
            return redirect('task')
        except ValueError:
          return render(request, 'task_detail.html', {'task':tarea,
                                                    'form': form,
                                                    'error':"The task could not be updated",
                                                    })
@login_required
def complete_task(request,taskid):
    tarea = get_object_or_404(Task, pk=taskid, user=request.user)
    if request.method == 'POST':
        tarea.datecompleted = timezone.now()
        tarea.save()
        return redirect('task')

@login_required
def delete_task(request,taskid):
    tarea = get_object_or_404(Task, pk=taskid, user=request.user)
    if request.method == 'POST':
        tarea.delete()
        return redirect('task')

@login_required
def list_completed_task(request):
        tasklist = Task.objects.filter(user_id=request.user, datecompleted__isnull=False).order_by('-datecompleted')
        print(tasklist)
        return render(request, 'complete_task.html' , {'listask': tasklist})
