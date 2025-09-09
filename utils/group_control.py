# utils/group_control.py

from core.score_manager import (
    list_permitted_groups as _list_permitted_groups,
    permit_group as _permit_group,
    revoke_group as _revoke_group,
)

def is_permitted(chat_id: int) -> bool:
    """
    Check if a chat_id is in the list of permitted groups.
    """
    return chat_id in _list_permitted_groups()

def permit_group(chat_id: int) -> None:
    """
    Add a chat_id to the permitted groups list.
    """
    _permit_group(chat_id)

def revoke_group(chat_id: int) -> None:
    """
    Remove a chat_id from the permitted groups list.
    """
    _revoke_group(chat_id)

def list_permitted_groups() -> list:
    """
    Return all chat_ids currently permitted.
    """
    return _list_permitted_groups()