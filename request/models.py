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
    
    class Meta:
        ordering = ('-time',)
    
    def __unicode__(self):
        return u'[%s] %s %s %s' % (self.time, self.method, self.path, self.response)
    
    def from_http_request(self, request, response=None, commit=True):
        # Request infomation
        self.method = request.method
        self.path = request.path
        
        self.is_secure = request.is_secure()
        self.is_ajax = request.is_ajax()
        
        # User infomation
        self.ip = request.META.get('REMOTE_ADDR', '')
        self.referer = request.META.get('HTTP_REFERER', '')
        self.user_agent = request.META.get('HTTP_USER_AGENT', '')
        self.language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        
        if request.user.is_authenticated():
            self.user = request.user
        
        if response:
            self.response = response.status_code
            
            if (response.status_code == 301) or (response.status_code == 302):
                self.redirect = response['Location']
        
        if commit:
            self.save()
