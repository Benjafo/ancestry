import os
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument('--username', help="Admin's username")
        parser.add_argument('--email', help="Admin's email")
        parser.add_argument('--password', help="Admin's password")

    def handle(self, *args, **options):
        User = get_user_model()

        if all([options[k] is None for k in 'username email password'.split()]):
            options['username'] = os.environ['DJANGO_SUPERUSER_USERNAME']
            options['email'] = os.environ['DJANGO_SUPERUSER_EMAIL']
            options['password'] = os.environ['DJANGO_SUPERUSER_PASSWORD']

        if not User.objects.filter(username=options['username']).exists():
            User.objects.create_superuser(username=options['username'],
                                          email=options['email'],
                                          password=options['password'])

        group, created = Group.objects.get_or_create(name='Admins')
        User.objects.get(username=options['username']).groups.add(group)