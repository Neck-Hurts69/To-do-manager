from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Team(models.Model):
    team_lead = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='member_list')
    due_date = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('progress', 'In Progress'),
        ('done', 'Done'),
    ]
    PRIORITY_CHOICES = [
        (3, 'High'),
        (2, 'Medium'),
        (1, 'Low'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='tasks_responsible')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks_team')
    is_completed = models.BooleanField(default=False)

    def is_overdue(self):
        if self.due_date and not self.is_completed:
            return self.due_date < timezone.now()
        return False

    def __str__(self):
        return self.title

class Project(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=200)
    description = models.TextField()
    tasks = models.ManyToManyField(Task)
    start_date = models.DateTimeField(blank=True, null=True)

    def start(self):
        self.start_date = timezone.now()
        self.save()
    
    def __str__(self):
        return self.project_title

class MultiTeamProject(models.Model):
    teams = models.ManyToManyField(Team)
    project_title = models.CharField(max_length=200)
    description = models.TextField()
    tasks = models.ManyToManyField(Task)
    start_date = models.DateTimeField(blank=True, null=True)
    due_date = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def is_overdue(self):
        if self.due_date and not self.is_completed:
            return self.due_date < timezone.now()
        return False
    
    def start(self):
        self.start_date = timezone.now()
        self.save()
    
    def __str__(self):
        return self.project_title