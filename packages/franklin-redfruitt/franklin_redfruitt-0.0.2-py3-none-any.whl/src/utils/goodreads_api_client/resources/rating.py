# -*- coding: utf-8 -*-
"""Module containing rating resource class."""

from src.utils.goodreads_api_client.exceptions import OauthEndpointNotImplemented
from src.utils.goodreads_api_client.resources.base import Resource


class Rating(Resource):
    resource_name = 'rating'

    def create(self):
        raise OauthEndpointNotImplemented('rating.create')

    def destroy(self):
        raise OauthEndpointNotImplemented('rating.destroy')
