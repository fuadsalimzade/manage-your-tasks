from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .forms import TodoForm
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import Task
from django.utils import timezone
from django.db import models


def signupuser(request):
    if request.method == "GET":
        return render(request, "task/signupuser.html", {"form": UserCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("currenttasks")

            except IntegrityError:
                return render(
                    request,
                    "task/signupuser.html",
                    {
                        "form": UserCreationForm(),
                        "error": "That username has been taken",
                    },
                )
        else:
            return render(
                request,
                "task/signupuser.html",
                {
                    "form": UserCreationForm(),
                    "error": "Please make sure that passwords are matching",
                },
            )


def loginuser(request):
    if request.method == "GET":
        return render(request, "task/loginuser.html", {"form": AuthenticationForm()})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user != None:
            login(request, user)
            return redirect("currenttasks")
        else:
            return render(
                request,
                "task/loginuser.html",
                {
                    "form": AuthenticationForm(),
                    "error": "This user profile does not exist. Please sign up.",
                },
            )


def createtask(request):
    if request.method == "GET":
        return render(request, "task/createtask.html", {"form": TodoForm()})
    else:
        if request.user.is_authenticated:
            try:
                form = TodoForm(request.POST)
                newtodo = form.save(commit=False)
                newtodo.user = request.user
                newtodo.save()
                return redirect("currenttasks")
            except ValueError:
                return render(
                    request,
                    "task/createtask.html",
                    {
                        "form": TodoForm(),
                        "error": "Bad data passed in. Try again",
                    },
                )
        else:
            return render(
                request,
                "task/createtask.html",
                {
                    "form": TodoForm(),
                    "error": "Please login or sign up before a creating a new task",
                },
            )


def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")


def currenttasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "task/currenttasks.html", {"tasks": tasks})

def currenttask(request, task_pk):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    task = get_object_or_404(tasks, pk=task_pk)
    if request.method == "GET":
        form = TodoForm(instance=task)
        return render(request, "task/currenttask.html", {"task": task,"form": form})
    elif request.method == "POST":
        try:
            form = TodoForm(request.POST, instance=task)
            form.save()
            return redirect("currenttasks")
        except ValueError:
            return render(request, "task/currenttask.html", 
                          {
                              "task": task,
                              "form": form,
                              "error": "Bad data passed in. Try again"})


def completecurrenttask(request, task_pk):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    task = get_object_or_404(tasks, pk=task_pk)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect("currenttasks")
    
def deletecurrenttask(request, task_pk):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    task = get_object_or_404(tasks, pk=task_pk)
    if request.method == "POST":
        task.delete()
        return redirect("currenttasks")

def completedtasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request, "task/completedtasks.html", {"tasks": tasks})

def completedtask(request, task_pk):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False)
    task = get_object_or_404(tasks, pk=task_pk)
    form = TodoForm(instance=task, editable = False)
    return render(request, "task/completedtask.html", {"form": form, "task": task})



def home(request):
    return render(request, "task/home.html")
