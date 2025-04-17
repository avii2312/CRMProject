from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Client(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField(unique=True)
    contact_phone = models.CharField(max_length=10, blank=True)
    company = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')

    def __str__(self):
        return self.name

class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    team = models.ForeignKey('accounts.Team', on_delete=models.SET_NULL, null=True, blank=True)
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Ticket(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    team = models.ForeignKey('accounts.Team', on_delete=models.SET_NULL, null=True, blank=True)
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='created_tickets',
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='updated_tickets',
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
