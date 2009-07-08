from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from request.utils import HTTP_STATUS_CODES

class Request(models.Model):
    # Response infomation
    response = models.SmallIntegerField(choices=HTTP_STATUS_CODES, default=200)
    
    # Request infomation
    method = models.CharField(default='GET', max_length=7)
    path = models.CharField(max_length=255)
    time = models.DateTimeField(default=datetime.now)
    
    is_secure = models.BooleanField(default=False)
    is_ajax = models.BooleanField(default=False)
    
    # User infomation
    ip = models.IPAddressField()
    user = models.ForeignKey(User, blank=True, null=True)
    referer = models.URLField(verify_exists=False, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=25, blank=True, null=True)
