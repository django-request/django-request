# -*- coding: utf-8 -*-
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone, six
from request.models import Request

DURATION_OPTIONS = {
    'hours': lambda amount: timezone.now() - timedelta(hours=amount),
    'days': lambda amount: timezone.now() - timedelta(days=amount),
    'weeks': lambda amount: timezone.now() - timedelta(weeks=amount),
    'months': lambda amount: timezone.now() - timedelta(days=(30 * amount)),  # 30-day month
    'years': lambda amount: timezone.now() - timedelta(weeks=(52 * amount)),  # 364-day year
}

input = raw_input if six.PY2 else input  # @ReservedAssignment


class Command(BaseCommand):
    help = "Purge old requests."

    def add_arguments(self, parser):
        parser.add_argument(
            'amount',
            type=int,
        )
        parser.add_argument('duration')
        parser.add_argument(
            '--noinput',
            action='store_false',
            dest='interactive',
            default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'
        )

    def handle(self, *args, **options):
        amount = options['amount']
        duration = options['duration']

        # Check we have the correct values
        if duration[-1] != 's':  # If its not plural, make it plural
            duration_plural = '%ss' % duration
        else:
            duration_plural = duration

        if duration_plural not in DURATION_OPTIONS:
            print('Amount must be %s' % ', '.join(DURATION_OPTIONS))
            return

        qs = Request.objects.filter(time__lte=DURATION_OPTIONS[duration_plural](amount))
        count = qs.count()

        if count == 0:
            print("There are no requests to delete.")
            return

        if options.get('interactive'):
            confirm = input("""
You have requested a database reset.
This will IRREVERSIBLY DESTROY any
requests created before %d %s ago.
That is a total of %d requests.
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: """ % (amount, duration, count))
        else:
            confirm = 'yes'

        if confirm == 'yes':
            qs.delete()
        else:
            print('Purge cancelled')
