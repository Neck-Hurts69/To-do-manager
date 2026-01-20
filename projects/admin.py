from django.contrib import admin
from django.utils import timezone
from .models import Team, Task, Project


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "team_lead", "due_date", "is_completed", "created_at", "member_count")
    search_fields = ("name", "members", "team_lead__username", "team_lead__email")
    list_filter = ("is_completed", "created_at", "due_date", "team_lead")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    def member_count(self, obj):
        if not obj.members:
            return 0
        return len([m.strip() for m in obj.members.split(",") if m.strip()])

    member_count.short_description = "Members count"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "team", "responsible", "status", "due_date", "is_completed", "overdue_badge")
    search_fields = ("title", "description", "team__name", "responsible__username", "responsible__email")
    list_filter = ("status", "is_completed", "due_date", "team", "responsible")
    ordering = ("due_date", "status")
    list_select_related = ("team", "responsible")
    actions = ("mark_completed", "mark_uncompleted")

    def overdue_badge(self, obj):
        return "❌ Overdue" if obj.is_overdue() else "—"

    overdue_badge.short_description = "Overdue?"

    def mark_completed(self, request, queryset):
        queryset.update(is_completed=True, status="done")

    def mark_uncompleted(self, request, queryset):
        queryset.update(is_completed=False)

    mark_completed.short_description = "Mark selected tasks as completed"
    mark_uncompleted.short_description = "Mark selected tasks as NOT completed"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "project_title", "team", "start_date", "task_count")
    search_fields = ("project_title", "description", "team__name", "tasks__title")
    list_filter = ("start_date", "team")
    filter_horizontal = ("tasks",)
    list_select_related = ("team",)
    ordering = ("-start_date",)

    def task_count(self, obj):
        return obj.tasks.count()

    task_count.short_description = "Number of tasks"
