# -*- coding: utf-8 -*-
"""Module containing review resource class."""

from src.utils.goodreads_api_client.exceptions import OauthEndpointNotImplemented
from src.utils.goodreads_api_client.resources.base import Resource


class Review(Resource):
    resource_name = 'review'

    def create(self):
        raise OauthEndpointNotImplemented('review.create')

    def destroy(self):
        raise OauthEndpointNotImplemented('review.destroy')

    def edit(self):
        raise OauthEndpointNotImplemented('review.edit')

    def list(self):
        raise OauthEndpointNotImplemented('review.list')

    def recent_reviews(self):
        endpoint = 'review/recent_reviews'
        res = self._transport.req(endpoint=endpoint)
        return res['reviews']

    def show(self, id_: str):
        return self._show_single_resource(id_)

    def show_by_user_and_book(self, user_id: str, book_id: str,
                              include_review_on_work: bool=False):
        endpoint = 'review/show_by_user_and_book'
        params = {
            'book_id': book_id,
            'include_review_on_work': include_review_on_work,
            'user_id': user_id,
        }
        res = self._transport.req(endpoint=endpoint, params=params)
        return res['review']
