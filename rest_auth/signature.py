# -*- coding: utf-8 -*-
from datetime import datetime
from django.conf import settings

from fost_authn.signature import fost_hmac_request_signature_with_headers

def get_signature(key_for_secret, method, path, timestamp, signed_headers_value=[], body=''):
    secret = settings.FOST_AUTHN_GET_SECRET(key_for_secret,'secret')

    document, signature = fost_hmac_request_signature_with_headers(
        secret,method,path,timestamp,signed_headers_value,body)

    return document, signature