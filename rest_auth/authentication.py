# -*- coding: utf-8 -*-
# ToDo: Move this to a library
import urllib
from datetime import datetime
from requests.auth import AuthBase
from fost_authn.signature import fost_hmac_request_signature_with_headers

from django.conf import settings

class FostAuth(AuthBase):
    """
    Attaches information for Fost authentication to the requested service
    """
    def __init__(self, username):
        """
        setup any auth-related data here
        """
        self.username = username

    def __call__(self, request):
        """
        modify and return the request
        """
        secret = settings.FOST_AUTHN_GET_SECRET(request,'secret')
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        path = unicode(request.path_url.split('?')[0])
        body = urllib.urlencode(request.data)
        document, signature = fost_hmac_request_signature_with_headers(
            secret,request.method,path,timestamp,[self.username,],body)

        request.headers['X-FOST-User'] = self.username
        request.headers['X-FOST-Headers'] = 'X-FOST-User'
        request.headers['X-FOST-Timestamp'] = timestamp
        request.headers['Authorization'] = 'FOST %s:%s' % (self.username,signature)
        return request