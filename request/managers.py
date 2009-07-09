from datetime import timedelta, datetime
from django.db import models
from django.contrib.auth.models import User

class RequestManager(models.Manager):
    def active_users(self, **options):
        """
        Returns a list of active users.
        
        Any arguments passed to this method will be
        given to timedelta for time filtering.
        
        Example:
        >>> Request.object.active_users(minutes=15)
        [<User: kylef>, <User: krisje8>]
        """
        
        qs = self.filter(user__isnull=False)
        
        if options:
            time = datetime.now() - timedelta(**options)
            qs = qs.filter(time__gte=time)
        
        requests = qs.select_related('user').only('user')
        
        users = []
        done = []
        
        for request in requests:
            if not (request.user.pk in done):
                done.append(request.user.pk)
                users.append(request.user)
        
        return users
