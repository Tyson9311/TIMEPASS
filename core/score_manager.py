import os
import json

FILE = os.path.join(os.path.dirname(__file__), "..", "data", "permissions.json")

def _load():
    if not os.path.exists(FILE):
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump({
                "sudos": [],
                "banned": [],
                "permitted_groups": [],
                "scores": {}
            }, f)
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(d: dict):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2)

# Permissions
def add_sudo(uid: str):
    d = _load()
    if uid in d["sudos"]:
        raise ValueError
    d["sudos"].append(uid)
    _save(d)

def remove_sudo(uid: str):
    d = _load()
    d["sudos"].remove(uid)
    _save(d)

def list_sudos():
    return _load()["sudos"]

def ban_user(uid: str):
    d = _load()
    if uid in d["banned"]:
        raise ValueError
    d["banned"].append(uid)
    _save(d)

def unban_user(uid: str):
    d = _load()
    d["banned"].remove(uid)
    _save(d)

def list_banned():
    return _load()["banned"]

def permit_group(chat_id: int):
    d = _load()
    if chat_id in d["permitted_groups"]:
        raise ValueError
    d["permitted_groups"].append(chat_id)
    _save(d)

def revoke_group(chat_id: int):
    d = _load()
    d["permitted_groups"].remove(chat_id)
    _save(d)

def list_permitted_groups():
    return _load()["permitted_groups"]

# Stats
def _ensure_user(d: dict, uid: str):
    if uid not in d["scores"]:
        d["scores"][uid] = {"games_played": 0, "wins": 0}

def record_game_end(participants: list, winner_id: str):
    d = _load()
    for uid in participants:
        _ensure_user(d, str(uid))
        d["scores"][str(uid)]["games_played"] += 1
    w = str(winner_id)
    _ensure_user(d, w)
    d["scores"][w]["wins"] += 1
    _save(d)

def get_stats(uid: str):
    return _load()["scores"].get(str(uid), {"games_played": 0, "wins": 0})

def get_leaderboard():
    sc = _load()["scores"]
    board = []
    for uid, v in sc.items():
        gp, w = v["games_played"], v["wins"]
        rate = (w/gp*100) if gp else 0
        board.append((uid, gp, w, rate))
    board.sort(key=lambda x: (x[3], x[2], x[1]), reverse=True)
    return board[:10]
