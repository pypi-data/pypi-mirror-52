"""
interface api;
"""
from typing import Optional


class User:

    def __init__(self, stored):
        self.stored = stored

    def has_permission(self, user: str, block: str, action: Optional[str] = None) -> bool:
        """
        check the user has the action permission for the block.
        :param user:
        :param block:
        :param action:
        :return:
        """
        return self.stored.has_permission(user, block, action)
