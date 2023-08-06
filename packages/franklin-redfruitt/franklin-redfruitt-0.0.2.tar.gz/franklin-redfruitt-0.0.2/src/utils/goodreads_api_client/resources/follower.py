# -*- coding: utf-8 -*-
"""Module containing follower resource class."""

from src.utils.goodreads_api_client.exceptions import OauthEndpointNotImplemented
from src.utils.goodreads_api_client.resources.base import Resource


class Follower(Resource):
    def create(self):
        raise OauthEndpointNotImplemented('follower.create')

    def destroy(self):
        raise OauthEndpointNotImplemented('follower.create')
