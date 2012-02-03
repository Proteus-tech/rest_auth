# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden

from rest_auth.signature import get_signature

@login_required
def signature(request):
    if not request.method == "GET":
        return HttpResponseNotAllowed(['GET'])

    params = request.GET.copy()

    if request.user.username != params.get('current_user'):
        return HttpResponseForbidden('You do not have permission to do this action.')

    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    document, generated_signature = get_signature('anything', params['method'], params['path'],
                                                    timestamp, [params['current_user'],])

    generated_signature = '%sTIME%s' % (generated_signature,timestamp)

    return HttpResponse(generated_signature)