from django.contrib import admin
from django.utils import timezone
from datetime import datetime
from django.utils import timezone
from .models import Task, Project, Team

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'team',
        'responsible',
        'due_date',
        'task_status',
        'is_completed',
    )

    list_filter = (
        'team',
        'responsible',
        'is_completed',
        'due_date',
    )

    search_fields = (
        'title',
        'description',
    )

    readonly_fields = (
        'created_at',
    )

    actions = ['mark_completed', 'mark_uncompleted']

    def task_status(self, obj):
        if obj.is_completed:
            return "✅ Completed"
        if obj.due_date and obj.due_date < timezone.now().date():
            return "❌ Overdue"
        return "⏳ In progress"

    task_status.short_description = "Status"

    def mark_completed(self, request, queryset):
        queryset.update(is_completed=True)

    def mark_uncompleted(self, request, queryset):
        queryset.update(is_completed=False)

    mark_completed.short_description = "Mark selected tasks as completed"
    mark_uncompleted.short_description = "Mark selected tasks as NOT completed"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'project_title',
        'team',
        'start_date',
        'task_count',
    )

    list_filter = (
        'team',
        'start_date',
    )

    search_fields = (
        'project_title',
        'description',
    )

    filter_horizontal = (
        'tasks',
    )

    def task_count(self, obj):
        return obj.tasks.count()

    task_count.short_description = "Number of tasks"

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'team_lead',
        'member_count',
    )

    list_filter = (
        'team_lead',
    )

    search_fields = (
        'name',
        'members',
    )

    def member_count(self, obj):
        return len(obj.members.split(',')) if obj.members else 0

    member_count.short_description = "Members count"
