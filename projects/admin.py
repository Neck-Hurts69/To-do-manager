from django.contrib import admin
from .models import Team
from .models import Task
from .models import Project

admin.site.register(Team)
admin.site.register(Task)
admin.site.register(Project)