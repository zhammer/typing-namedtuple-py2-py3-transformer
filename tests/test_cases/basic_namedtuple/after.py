"""
A basic python2 namedtuple.
"""
from typing import NamedTuple
import six


class User(NamedTuple):
    id: int
    first_name: six.text_type
    last_name: six.text_type
