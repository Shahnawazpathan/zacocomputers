from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, TaskForm
from .models import Task
from django.contrib.auth.models import User

@login_required
def index(request):
    return render(request, 'index.html', {'title': 'index'})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form, 'title': 'register here'})

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {username}!!')
            return redirect('index')
        else:
            messages.info(request, f'Account does not exist, please sign in')
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'title': 'log in'})

@login_required
def mytask(request):
    tasks_assigned_to_me = Task.objects.filter(assigned_to=request.user)    
    return render(request, 'mytask.html', {'tasks_assigned_to_me': tasks_assigned_to_me})

@login_required
def created_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('create_task')
    else:
        form = TaskForm()
    my_tasks = Task.objects.filter(user=request.user)
    return render(request, 'todo.html', { 'my_tasks': my_tasks , 'form1': form})

@login_required
def delete_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.filter(id=task_id).delete()
        messages.success(request, 'Task deleted successfully.')
    return redirect('create_task')

@login_required
def status(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        new_status = request.POST.get('status')
        if new_status == "completed":
            task.completed = True
        else:
            task.completed = False
        task.save()  
        messages.success(request, f'Task status updated to {new_status}.')
        return redirect('my_task')  

    return redirect('my_task')

@login_required
def checker(request):
    result = None

    if request.method == 'POST':
        year = request.POST.get('year')
        if year:
            try:
                year = int(year)
                if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                    result = f'{year} is a leap year.'
                else:
                    result = f'{year} is not a leap year.'
            except ValueError:
                result = 'Invalid input. Please enter a valid year.'

    return render(request, 'leepyear.html', {'result': result})
