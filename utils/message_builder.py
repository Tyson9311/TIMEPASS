import time
from core.settings import TURN_TIMER
from core.game_session import GameSession

def build_turn_prompt(session: GameSession) -> str:
    cid    = session.order[0]
    nid    = session.order[1] if len(session.order) > 1 else None
    me     = session.players[cid]["name"]
    mm     = f"[{me}](tg://user?id={cid})"
    nn     = session.players[nid]["name"] if nid else "—"
    alive  = len(session.order)
    total  = session.initial_player_count
    dur    = session.format_duration(time.time() - session.start_time)
    return (
        f"Turn: {mm} (Next: {nn})\n"
        f"Mode: {session.current_mode_type.title()} ({session.current_mode_param})\n"
        f"Players remaining: {alive}/{total}\n"
        f"Time per turn: {TURN_TIMER}s\n"
        f"Total words so far: {session.total_submissions}\n"
        f"Game duration: {dur}"
    )
