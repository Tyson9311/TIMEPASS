import time
from config import MAX_PLAYERS

# Active sessions: chat_id → GameSession
sessions = {}

class GameSession:
    def __init__(self, chat_id):
        self.chat_id            = chat_id
        self.players            = {}    # uid → {"name": str}
        self.order              = []    # turn order
        self.current_mode_type  = None
        self.current_mode_param = None
        self.start_letter       = None

        # lobby phase
        self.join_jobs     = []
        self.join_end_time = None

        # turn phase
        self.start_time            = None
        self.turn_start_time       = None
        self.elimination_job       = None
        self.last_word             = None
        self.total_submissions     = 0
        self.initial_player_count  = 0

    def add_player(self, uid, name):
        if uid in self.players or len(self.players) >= MAX_PLAYERS:
            return False
        self.players[uid] = {"name": name}
        return True

    def remove_player(self, uid):
        self.players.pop(uid, None)

    def start(self):
        self.initial_player_count = len(self.players)
        self.order = list(self.players.keys())
        self.start_time = time.time()
        self.last_word = None
        self.total_submissions = 0

    def eliminate(self, uid):
        self.players.pop(uid, None)
        if uid in self.order:
            self.order.remove(uid)

    def next_turn(self):
        self.order.append(self.order.pop(0))

    def format_duration(self, seconds):
        m, s = divmod(int(seconds), 60)
        return f"{m}m{s}s"