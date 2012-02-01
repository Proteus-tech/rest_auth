# -*- coding: utf-8 -*-
import urllib
from datetime import datetime
from django.conf import settings
from fost_authn.signature import fost_hmac_request_signature_with_headers

class AjaxUserMiddleware(object):
    def process_request(self,request):
        if not request.user.username:
            current_user = ''
            if request.method == "GET":
                current_user = request.GET.get('current_user')
            elif request.method == "POST":
                current_user = request.POST.get('current_user')
            if current_user:
                secret = settings.FOST_AUTHN_GET_SECRET(request,'secret')
                timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

                path = request.path
                body = request.raw_post_data
                document, signature = fost_hmac_request_signature_with_headers(
                    secret,request.method,path,timestamp,[current_user,],body)

                request.META['HTTP_X_FOST_USER'] = current_user
                request.META['HTTP_X_FOST_HEADERS'] = 'X-FOST-User'
                request.META['HTTP_X_FOST_TIMESTAMP'] = timestamp
                request.META['HTTP_AUTHORIZATION'] = 'FOST %s:%s' % (current_user,signature)