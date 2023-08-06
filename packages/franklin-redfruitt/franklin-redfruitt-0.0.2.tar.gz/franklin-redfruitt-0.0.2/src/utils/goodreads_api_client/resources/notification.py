# -*- coding: utf-8 -*-
"""Module containing notification resource class."""

from src.utils.goodreads_api_client.exceptions import OauthEndpointNotImplemented
from src.utils.goodreads_api_client.resources.base import Resource


class Notification(Resource):
    def view(self):
        raise OauthEndpointNotImplemented('notifications')
