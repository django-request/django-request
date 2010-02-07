from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from request.managers import RequestManager
from request.utils import HTTP_STATUS_CODES, browsers, engines

class Request(models.Model):
    # Response infomation
    response = models.SmallIntegerField(_('response'), choices=HTTP_STATUS_CODES, default=200)
    
    # Request infomation
    method = models.CharField(_('method'), default='GET', max_length=7)
    path = models.CharField(_('path'), max_length=255)
    time = models.DateTimeField(_('time'), default=datetime.now)
    
    is_secure = models.BooleanField(_('is secure'), default=False)
    is_ajax = models.BooleanField(_('is ajax'), default=False, help_text=_('Wheather this request was used via javascript.'))
    
    # User infomation
    ip = models.IPAddressField(_('ip address'))
    user = models.ForeignKey(User, blank=True, null=True)
    referer = models.URLField(_('referer'), verify_exists=False, max_length=255, blank=True, null=True)
    user_agent = models.CharField(_('user agent'), max_length=255, blank=True, null=True)
    language = models.CharField(_('language'), max_length=255, blank=True, null=True)
    
    objects = RequestManager()
    
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
        self.referer = request.META.get('HTTP_REFERER', '')[:255]
        self.user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
        self.language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')[:255]
        
        if getattr(request, 'user', False):
            if request.user.is_authenticated():
                self.user = request.user
        
        if response:
            self.response = response.status_code
            
            if (response.status_code == 301) or (response.status_code == 302):
                self.redirect = response['Location']
        
        if commit:
            self.save()
    
    #@property
    def browser(self):
        if not self.user_agent:
            return
        
        if not hasattr(self, '_browser'):
            self._browser = browsers.resolve(self.user_agent)
        return self._browser[0]
    browser = property(browser)
    
    #@property
    def keywords(self):
        if not self.referer:
            return
        
        if not hasattr(self, '_keywords'):
            self._keywords = engines.resolve(self.referer)
        if self._keywords:
            return ' '.join(self._keywords[1]['keywords'].split('+'))
    keywords = property(keywords)
