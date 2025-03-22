from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=255) 
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  
    members = models.ManyToManyField(User, related_name="teams", blank=True)  

class Board(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards', default=1)
    team  = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='teamboards', default=1)

class List(models.Model):
    name = models.CharField(max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists')
    created_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    name = models.CharField(max_length=255) 
    description = models.TextField(blank=True, null=True) 
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="tasks")  
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False) 
    start_date = models.DateTimeField(blank=True, null=True)  
    end_date = models.DateTimeField(blank=True, null=True) 
    due_date = models.DateTimeField(blank=True, null=True)  
    assigned_users = models.ManyToManyField(User, related_name="assigned_tasks", blank=True)


