# -*- coding: utf-8 -*-
from datetime import datetime
from rest_auth.signature import get_signature

from django import template
register = template.Library()

@register.simple_tag
def get_signature_for_cross_origin_call(method, path, current_user):
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    document, signature = get_signature('anything', method, path, timestamp, signed_headers_value=[current_user,])
    return '%sTIME%s' % (signature,timestamp)