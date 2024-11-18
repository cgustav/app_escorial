from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Reset passwords for all users or specific users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            default='password123',
            help='New password to set for all users'
        )
        parser.add_argument(
            '--users',
            nargs='+',
            help='Usernames to reset (optional, if not provided will reset all)'
        )

    def handle(self, *args, **options):
        new_password = options['password']
        specific_users = options['users']

        if specific_users:
            users = User.objects.filter(username__in=specific_users)
        else:
            users = User.objects.all()

        for user in users:
            user.password = make_password(new_password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully reset password for user: {user.username}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'New password is: {new_password}')
            )

        self.stdout.write(
            self.style.SUCCESS(f'Reset {users.count()} user passwords')
        )