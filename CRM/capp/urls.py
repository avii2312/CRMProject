from django.urls import path
from .views import (
    ClientListView, ClientDetailView,
    ProjectListView,
    TicketListView, ProjectDetailView,
)
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('tickets/', TicketListView.as_view(), name='ticket_list'),
]

# path('login/', auth_views.LoginView.as_view(template_name='crm/login.html'), name='login'),
# path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

# CRM views