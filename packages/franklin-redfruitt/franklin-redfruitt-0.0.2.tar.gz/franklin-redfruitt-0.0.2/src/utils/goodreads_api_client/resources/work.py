# -*- coding: utf-8 -*-
"""Module containing work resource class."""

from src.utils.goodreads_api_client.exceptions import ExtraApiPermissionsRequired
from src.utils.goodreads_api_client.resources.base import Resource


class Work(Resource):
    def editions(self, id_: str):
        raise ExtraApiPermissionsRequired('work.editions')
