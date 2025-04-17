from django.contrib import admin
from .models import Client, Project, Ticket

admin.site.register(Client)
admin.site.register(Project)
admin.site.register(Ticket)
