from datetime import datetime
from collections import defaultdict
import ipdb

def to_minutes(dt_str, base_time):
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    delta = dt - base_time
    return delta.days * 24 * 60 + delta.seconds // 60

def validate_and_score(data, assignments):
    games = {g["game_id"]: g for g in data["games"]}
    referees = {r["referee_id"]: r for r in data["referees"]}
    base_time = datetime.strptime(data["games"][0]["time_begin"], "%Y-%m-%d %H:%M:%S")

    referee_roles = defaultdict(list)
    referee_schedule = defaultdict(list)
    total_score = 0
    is_valid = True
    errors = []

    for a in assignments:
        gid = a["game_id"]
        game = games[gid]
        start = to_minutes(game["time_begin"], base_time)
        end = to_minutes(game["time_end"], base_time)
        field = game["field"]
        level = game["level_factor"]

        refs = {
            "main": a["main_referee"],
            "assistant1": a["assistant_referees"][0],
            "assistant2": a["assistant_referees"][1],
            "fourth": a["fourth_official"]
        }

        if len(set(refs.values())) < 4:
            is_valid = False
            errors.append(f"Referees not unique in game {gid}")

        for role, rid in refs.items():
            ref = referees.get(rid)
            if not ref:
                is_valid = False
                errors.append(f"Referee {rid} not found")
                continue

            # Check availability
            available = any(
                to_minutes(slot["from"], base_time) <= start and to_minutes(slot["to"], base_time) >= end
                for slot in ref["available_slots"]
            )
            if not available:
                is_valid = False
                errors.append(f"Referee {rid} not available for game {gid}")

            referee_roles[rid].append((gid, role))
            referee_schedule[rid].append((start, end, field, gid))

            # Add score
            if role == "main":
                total_score += ref["main_referee_experience"] * level
            elif role.startswith("assistant"):
                total_score += ref["assistant_referee_experience"] * level

    # Fatigue limit
    for rid, roles in referee_roles.items():
        main_assist_count = sum(1 for _, role in roles if role.startswith("main") or role.startswith("assistant"))
        if main_assist_count > 2:
            is_valid = False
            errors.append(f"Referee {rid} over fatigue limit ({main_assist_count} roles)")

    # Overlaps and travel time
    for rid, slots in referee_schedule.items():
        slots.sort()
        for i in range(len(slots) - 1):
            s1, e1, f1, g1 = slots[i]
            s2, e2, f2, g2 = slots[i + 1]
            if e1 > s2:
                is_valid = False
                errors.append(f"Referee {rid} has overlapping games {g1} and {g2}")
            elif f1 != f2 and e1 + 30 > s2:
                is_valid = False
                errors.append(f"Referee {rid} lacks 30-min travel between {g1} and {g2}")

    if not is_valid:
        total_score = 0

    return {
        "num_games": len(games),
        "valid": is_valid,
        "score": total_score,
        "errors": errors
    }
