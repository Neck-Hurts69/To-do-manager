from django.contrib import admin
from django.utils.html import format_html
from .models import Task, Team, Project

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','team','responsible',
                    'status','due_date','overdue_status','is_completed')
    list_filter = ('status','team','due_date',)
    search_fields = ('title','description',)
    ordering = ('due_date',)
    actions = ['mark_completed']

    def mark_completed(self, request, queryset):
        queryset.update(is_completed=True)
    mark_completed.short_description = "Mark selected tasks as completed"
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('team', 'responsible')
    def overdue_status(self, obj):
        if obj.is_overdue():
            return format_html('<span style="color:red; font-weight:bold;">Overdue</span>')
        return format_html('<span style="color:green;">On time</span>')

    overdue_status.short_description = "Deadline status"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'team', 'start_date')
    filter_horizontal = ('tasks',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_lead')