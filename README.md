## django-request

django-request is a statistics module for django. It stores requests in a database for admins to see, it can also be used to get statistics on who is online etc.

As well as a site statistics module, with the active_users template tag and manager method you can also use django-request to show who is online in a certain time.

    Request.objects.active_users(minutes=15)

### In development

django-request is not finished statistics program, currently it will only store requests and pull active users with a basic admin interface.

### Detailed documentation

For a detailed documentation of django-request please see: http://kylefuller.co.uk/projects/django-request/ or the docs/ directory.
