# -*- coding: utf-8 -*-
"""
goodreads_api_client.resources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Holds classes for each Goodreads API Resource a user can interact with via
the Goodreads API
"""

from src.utils.goodreads_api_client.resources.author import Author
from src.utils.goodreads_api_client.resources.author_following import AuthorFollowing
from src.utils.goodreads_api_client.resources.book import Book
from src.utils.goodreads_api_client.resources.comment import Comment
from src.utils.goodreads_api_client.resources.event import Event
from src.utils.goodreads_api_client.resources.follower import Follower
from src.utils.goodreads_api_client.resources.friend import Friend
from src.utils.goodreads_api_client.resources.group import Group
from src.utils.goodreads_api_client.resources.list import List
from src.utils.goodreads_api_client.resources.notification import Notification
from src.utils.goodreads_api_client.resources.owned_book import OwnedBook
from src.utils.goodreads_api_client.resources.quote import Quote
from src.utils.goodreads_api_client.resources.rating import Rating
from src.utils.goodreads_api_client.resources.read_status import ReadStatus
from src.utils.goodreads_api_client.resources.recommendation import Recommendation
from src.utils.goodreads_api_client.resources.review import Review
from src.utils.goodreads_api_client.resources.series import Series
from src.utils.goodreads_api_client.resources.shelf import Shelf
from src.utils.goodreads_api_client.resources.topic import Topic
from src.utils.goodreads_api_client.resources.update import Update
from src.utils.goodreads_api_client.resources.user import User
from src.utils.goodreads_api_client.resources.user_shelf import UserShelf
from src.utils.goodreads_api_client.resources.user_status import UserStatus
from src.utils.goodreads_api_client.resources.work import Work

__all__ = [
    'Author',
    'AuthorFollowing',
    'Book',
    'Comment',
    'Event',
    'Follower',
    'Friend',
    'Group',
    'List',
    'Notification',
    'OwnedBook',
    'Quote',
    'Rating',
    'ReadStatus',
    'Recommendation',
    'Review',
    'Series',
    'Shelf',
    'Topic',
    'Update',
    'User',
    'UserShelf',
    'UserStatus',
    'Work',
]
