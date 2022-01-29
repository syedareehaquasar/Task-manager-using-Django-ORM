from asyncio import tasks
from django.shortcuts import render
from django.http import HttpResponseRedirect

from tasks.models import Task

def task():
    return Task.objects.filter(deleted=False).filter(completed=False)

def completed_tasks():
    return Task.objects.filter(deleted=False).filter(completed=True)

def all_tasks_view(request):
    return render(
        request,
        "allTasks.html",
        {
            "tasks": task(),
            "completed_tasks": completed_tasks(),
        },
    )


def task_view(request):
    search_term = request.GET.get("search")
    tasks = task()
    if search_term:
        tasks = tasks.filter(title__icontains=search_term)
    return render(request, "tasks.html", {"tasks": tasks})


def completed_tasks_view(request):
    return render(request, "completedTasks.html", {"completed_tasks": completed_tasks()})


def add_task_view(request):
    task_value = request.GET.get("task")
    task_obj = Task(title=task_value)
    task_obj.save()
    return HttpResponseRedirect("/all_tasks")


def delete_task_view(request, index):
    Task.objects.filter(id=index).update(deleted=True)
    return HttpResponseRedirect("/all_tasks")


def complete_task_view(request, index):
    Task.objects.filter(id=index).update(completed=True)
    return HttpResponseRedirect("/all_tasks")
