# -*- coding: utf-8 -*-
"""Module containing update resource class."""

from src.utils.goodreads_api_client.exceptions import OauthEndpointNotImplemented
from src.utils.goodreads_api_client.resources.base import Resource


class Update(Resource):
    def friends(self):
        raise OauthEndpointNotImplemented('update.friends')
