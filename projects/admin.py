from django.contrib import admin
from django.utils.html import format_html
from .models import Task, Team, Project

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'team',
        'responsible',
        'status',
        'due_date',
        'overdue_status',
    )
    list_filter = ('status','team','due_date',)
    search_fields = ('title','description',)

admin.site.register(Team)
admin.site.register(Task)
admin.site.register(Project)