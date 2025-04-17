from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Client, Project, Ticket
from django.db.models import Q
from django.utils import timezone
from django.db.models import Count
import json
from actstream.models import Action



def dashboard_view(request):
    now = timezone.now()
    start_of_month = now.replace(day=1)

    # Initialize the context dictionary
    context = {}

    # Add data to the context
    context.update({
        'open_tickets_count': Ticket.objects.filter(status='open').count(),
        'projects_in_progress_count': Project.objects.filter(status='in_progress').count(),
        'new_clients_count': Client.objects.filter(created_at__gte=start_of_month).count(),
        # Add other context variables as needed
    })
    resolved_tickets = Ticket.objects.filter(status='resolved')
    resolution_times = [
        (ticket.resolved_at - ticket.created_at).days
        for ticket in resolved_tickets
        if ticket.resolved_at and ticket.created_at
    ]
    resolution_time_labels = [f'Ticket {ticket.id}' for ticket in resolved_tickets]
    resolution_time_data = resolution_times

    # For project statuses
    project_status_counts = Project.objects.values('status').annotate(count=Count('id'))
    project_status_labels = [item['status'] for item in project_status_counts]
    project_status_data = [item['count'] for item in project_status_counts]

    context.update({
        'resolution_time_labels': json.dumps(resolution_time_labels),
        'resolution_time_data': resolution_time_data,
        'project_status_labels': json.dumps(project_status_labels),
        'project_status_data': project_status_data,
    })
    recent_activities = Action.objects.order_by('-timestamp')[:10]

    context.update({
        'recent_activities': recent_activities,
    })

    return render(request, 'dashboard.html', context)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'capp/client_list.html'
    context_object_name = 'clients'
    paginate_by = 10  # optional

    def get_queryset(self):
        qs = Client.objects.filter(owner=self.request.user)
        q = self.request.GET.get('q', '').strip()
        company = self.request.GET.get('company', '').strip()

        if q:
            # search name or email
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(contact_email__icontains=q)
            )
        if company:
            qs = qs.filter(company__iexact=company)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # carry over filter values so the form keeps them
        ctx['q'] = self.request.GET.get('q', '')
        ctx['company'] = self.request.GET.get('company', '')
        # supply a list of companies for the dropdown
        ctx['company_list'] = (
            Client.objects
                  .filter(owner=self.request.user)
                  .values_list('company', flat=True)
                  .distinct()
                  .order_by('company')
        )
        return ctx


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'capp/client_detail.html'
    context_object_name = 'client'

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'capp/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        qs = Project.objects.all()
        client_id = self.request.GET.get('client_id')
        if client_id:
            qs = qs.filter(client__id=client_id)
        return qs

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'capp/project_detail.html'
    context_object_name = 'project'


# class TicketListView(LoginRequiredMixin, ListView):
#     model = Ticket
#     template_name = 'capp/ticket_list.html'
#     context_object_name = 'tickets'

    # def get_queryset(self):
    #     # Optionally filter tickets by project if passed as a parameter
    #     qs = Ticket.objects.all()
    #     project_id = self.request.GET.get('project_id')
    #     if project_id:
    #         qs = qs.filter(project__id=project_id)
    #     return qs

    # def get_queryset(self):
    #     user = self.request.user
    #     return Ticket.objects.filter(team__in=user.teams.all())
class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'capp/tickets_list.html'
    context_object_name = 'tickets'
    paginate_by = 10

    def get_queryset(self):
        qs = Ticket.objects.filter(team__in=self.request.user.teams.all())
        project_id = self.request.GET.get('project_id')

        # Only filter if project_id is a digit
        if project_id and project_id.isdigit():
            qs = qs.filter(project__id=int(project_id))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        project_id = self.request.GET.get('project_id')
        # Ensure project_id is numeric, otherwise treat as None
        ctx['project_id'] = project_id if project_id and project_id.isdigit() else ''
        ctx['project_list'] = Project.objects.filter(client__owner=self.request.user).order_by('title')
        return ctx
