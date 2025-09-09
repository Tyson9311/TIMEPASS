import os
import json

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "..", "data")
PREF = os.path.join(DATA, "prefix_dictionary.json")
SUFF = os.path.join(DATA, "suffix_dictionary.json")

def _ensure(path):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f)

# Prefix
_ensure(PREF)
with open(PREF, "r", encoding="utf-8") as f:
    prefix_dict = json.load(f)

def save_prefix():
    with open(PREF, "w", encoding="utf-8") as f:
        json.dump(prefix_dict, f, indent=2)

def add_prefix(p: str):
    key = p.lower()
    if key in prefix_dict:
        raise ValueError("exists")
    prefix_dict[key] = []
    save_prefix()

def remove_prefix(p: str):
    key = p.lower()
    if key not in prefix_dict:
        raise ValueError("not found")
    del prefix_dict[key]
    save_prefix()

def add_word_to_prefix(p: str, w: str):
    key, wkey = p.lower(), w.lower()
    if key not in prefix_dict:
        raise ValueError("prefix not found")
    if wkey in prefix_dict[key]:
        raise ValueError("word exists")
    prefix_dict[key].append(wkey)
    save_prefix()

def remove_word_from_prefix(p: str, w: str):
    key, wkey = p.lower(), w.lower()
    if key not in prefix_dict or wkey not in prefix_dict[key]:
        raise ValueError("not found")
    prefix_dict[key].remove(wkey)
    save_prefix()

# Suffix
_ensure(SUFF)
with open(SUFF, "r", encoding="utf-8") as f:
    suffix_dict = json.load(f)

def save_suffix():
    with open(SUFF, "w", encoding="utf-8") as f:
        json.dump(suffix_dict, f, indent=2)

def add_suffix(s: str):
    key = s.lower()
    if key in suffix_dict:
        raise ValueError("exists")
    suffix_dict[key] = []
    save_suffix()

def remove_suffix(s: str):
    key = s.lower()
    if key not in suffix_dict:
        raise ValueError("not found")
    del suffix_dict[key]
    save_suffix()

def add_word_to_suffix(s: str, w: str):
    key, wkey = s.lower(), w.lower()
    if key not in suffix_dict:
        raise ValueError("suffix not found")
    if wkey in suffix_dict[key]:
        raise ValueError("word exists")
    suffix_dict[key].append(wkey)
    save_suffix()

def remove_word_from_suffix(s: str, w: str):
    key, wkey = s.lower(), w.lower()
    if key not in suffix_dict or wkey not in suffix_dict[key]:
        raise ValueError("not found")
    suffix_dict[key].remove(wkey)
    save_suffix()