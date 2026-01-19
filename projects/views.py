from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from django.utils import timezone


@login_required(login_url='/admin/login/')  # Add this decorator
def task_list(request):
    if request.method == "POST":
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')
        Task.objects.create(
            title=title,
            due_date=due_date,
            responsible=request.user
        )
        return redirect('task_list')
    tasks = Task.objects.all()
    return render(request, '../templates/index.html', {'tasks': tasks})

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_completed = not task.is_completed
    task.save()
    if task.is_completed:
        messages.success(request, f'Задача "{task.title}" выполнена! 🎉')
    else:
        messages.info(request, f'Задача "{task.title}" снова в работе.')
    return redirect('task_list')


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    messages.warning(request, 'Задача удалена.')
    return redirect('task_list')