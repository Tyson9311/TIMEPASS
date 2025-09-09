from core.score_manager import list_sudos, list_banned
from config import OWNER_ID

def is_owner(uid: int):
    return uid == OWNER_ID

def is_sudo(uid: int):
    return str(uid) in list_sudos() or is_owner(uid)

def is_admin(uid: int):
    return is_sudo(uid)

def is_banned(uid: int):
    return str(uid) in list_banned()