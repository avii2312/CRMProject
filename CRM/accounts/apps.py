# accounts/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate

class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        # Import inside ready so models are loaded
        from django.contrib.auth.models import Group, Permission
        from django.db.models.signals import post_migrate

        def create_roles(sender, **kwargs):
            roles = {
                'Admin': ['add_client','change_client','delete_client','view_client',
                          'add_project','change_project','delete_project','view_project',
                          'add_ticket','change_ticket','delete_ticket','view_ticket'],
                'Manager': ['view_client','view_project','add_ticket','change_ticket','view_ticket'],
                'Agent': ['view_ticket','change_ticket']
            }
            for role_name, perms in roles.items():
                grp, _ = Group.objects.get_or_create(name=role_name)
                for codename in perms:
                    try:
                        perm = Permission.objects.get(codename=codename)
                        grp.permissions.add(perm)
                    except Permission.DoesNotExist:
                        pass

        # Connect after migrations are run
        post_migrate.connect(create_roles, sender=self)
