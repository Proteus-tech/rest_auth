# -*- coding: utf-8 -*-
# ToDo: Move this to a library
from fost_authn.authentication import FostBackend
from slumber.connector.authentication import Backend as SlumberBackend
from slumber.connector.authentication import _assert_properly_configured
from slumber import client
from slumber.connector.proxies import attach_to_local_user

from django.contrib.auth.models import User

class SlumberFostBackend(FostBackend, SlumberBackend):

    def get_user(self, user_id):
        """Return the user associated with the user_id specified.
        """
        _assert_properly_configured()
        try:
            try:
                local_user = User.objects.get(**{'username':user_id})
                remote_user =\
                client.auth.django.contrib.auth.User.get(
                    username=local_user.username)
            except User.DoesNotExist:
                remote_user =\
                client.auth.django.contrib.auth.User.get(**{'username':user_id})
        except AssertionError:
            return None
        return attach_to_local_user(remote_user)