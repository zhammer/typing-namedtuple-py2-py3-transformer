"""
A basic python2 namedtuple.
"""
from typing import NamedTuple
import six


User = NamedTuple(
    "User",
    [
        ("id", int),
        ("first_name", six.text_type),
        ("last_name", six.text_type)
    ]
)
