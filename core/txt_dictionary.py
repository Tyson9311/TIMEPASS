import os

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "..", "data")

def _path(mode: str):
    return os.path.join(DATA, f"{mode}.txt")

def load_words(mode: str):
    p = _path(mode)
    if not os.path.exists(p):
        open(p, "w", encoding="utf-8").close()
    with open(p, "r", encoding="utf-8") as f:
        return [l.strip().lower() for l in f if l.strip()]

def save_words(mode: str, words: list):
    p = _path(mode)
    unique = sorted(set(w.strip().lower() for w in words if w.strip()))
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(unique))

# NH dictionary
NH_PATH = os.path.join(DATA, "NH.txt")

def load_nh():
    if not os.path.exists(NH_PATH):
        open(NH_PATH, "w", encoding="utf-8").close()
    with open(NH_PATH, "r", encoding="utf-8") as f:
        return [l.strip().lower() for l in f if l.strip()]

def add_nh_word(w: str):
    w = w.strip().lower()
    words = load_nh()
    if w in words:
        raise ValueError("already exists")
    words.append(w)
    save_words("NH", words)

def remove_nh_word(w: str):
    w = w.strip().lower()
    words = load_nh()
    if w not in words:
        raise ValueError("not found")
    words.remove(w)
    save_words("NH", words)

def count_nh_words():
    return len(load_nh())