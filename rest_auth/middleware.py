# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.conf import settings
from rest_auth import signature as ra_signature # import like this for mocking in tests

import logging
logger = logging.getLogger(__name__)

class AjaxUserMiddleware(object):
    def authentication_headers_exist(self, request):
        headers = ['HTTP_X_FOST_USER','HTTP_X_FOST_HEADERS','HTTP_X_FOST_TIMESTAMP','HTTP_AUTHORIZATION']
        for header in headers:
            if not request.META.has_key(header):
                return False
        return True


    def process_request(self, request):
        if not request.user.username and not self.authentication_headers_exist(request):
            logger.info('path: %s' % request.path)
            time_format = '%Y-%m-%d %H:%M:%S'
            current_user = ''
            input_signature = ''
            signed_time = datetime.min
            params = request.GET.copy()

            if params:
                current_user = params.get('current_user')
                signed_value = params.get('signed_value')

                logger.info('current_user: %s' % current_user)
                logger.info('signed_value: %s' % signed_value)
                if signed_value:
                    splitted_signed_value = signed_value.split('TIME')
                    if len(splitted_signed_value) == 2:
                        input_signature = splitted_signed_value[0]

                        # because '+' will turn into space, we will replace all space with '+'
                        input_signature = input_signature.replace(' ','+')

                        signed_time = datetime.strptime(splitted_signed_value[1],time_format)

            utc_now = datetime.utcnow()
            delta = timedelta(0, getattr(settings,
                'FOST_AUTHN_MAXIMUM_CLOCK_SKEW', 300))
            skew = max(signed_time - utc_now, utc_now - signed_time)
            logger.info('skew: %s' % skew)
            if (skew < delta) and current_user and input_signature:
                path = request.path
                body = request.raw_post_data

                document, test_signature = ra_signature.get_signature(request,request.method,request.build_absolute_uri(path),signed_time,[current_user,])

                logger.info('input_signature: %s' % input_signature)
                logger.info('test_signature: %s' % test_signature)
                if input_signature == test_signature:
                    timestamp = datetime.utcnow().strftime(time_format)
                    # if they've passed this check, now it's time to put their user in so Fost authentication accepts
                    document, signature = ra_signature.get_signature(request,request.method,path,timestamp,[current_user,],body)

                    request.META['HTTP_X_FOST_USER'] = current_user
                    request.META['HTTP_X_FOST_HEADERS'] = 'X-FOST-User'
                    request.META['HTTP_X_FOST_TIMESTAMP'] = timestamp
                    request.META['HTTP_AUTHORIZATION'] = 'FOST %s:%s' % (current_user,signature)


