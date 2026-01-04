from django.conf import settings
from django.db import models
from django.utils import timezone

class Team(models.Model):
    team_lead = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    members = models.TextField()

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('progress', 'In Progress'),
        ('done', 'Done'),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')

    def is_overdue(self):
        return self.due_date and self.due_date < timezone.now().date() and self.status != 'done'
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