from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create test users'

    def handle(self, *args, **kwargs):
        users = [
            {'username': 'testuser1', 'email': 'test1@example.com',
             'password': 'password123'},
            {'username': 'testuser2', 'email': 'test2@example.com',
             'password': 'password123'},
        ]

        for user_data in users:
            if not User.objects.filter(username=user_data['username']).exists():
                User.objects.create_user(**user_data)
                self.stdout.write(self.style.SUCCESS(f"User {user_data['username']} created"))
            else:
                self.stdout.write(self.style.WARNING(f"User {user_data['username']} already exists"))