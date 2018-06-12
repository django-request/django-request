# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

from ...models import Request

try:
    # to keep backward Python 2 compatibility
    input = raw_input
except NameError:
    pass


class Command(BaseCommand):
    help = 'Purge user requests.'

    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument(
            '--noinput',
            action='store_false',
            dest='interactive',
            default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'
        )

    def handle(self, *args, **options):
        username = options['username']

        if username is None or username == '':
            raise CommandError('Please enter a valid username')

        qs = Request.objects.filter(user__username=username)
        count = qs.count()

        if count == 0:
            print('There are no requests to delete.')
            return

        if options.get('interactive'):
            confirm = input('''
You have requested to delete requests from user {0}.
That is a total of {1} requests.
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel:'''.format(username, count))
        else:
            confirm = 'yes'

        if confirm == 'yes':
            qs.delete()
        else:
            print('Purge cancelled')
