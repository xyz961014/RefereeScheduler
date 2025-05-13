import json
from datetime import datetime
from collections import defaultdict
import ipdb

def time_to_minutes(dt_str, time_baseline):
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S") - time_baseline
    return dt.days * 24 * 60 + dt.seconds // 60

def generate_dzn(data):
    games = data["games"]
    referees = data["referees"]
    
    assert len(games) > 0

    time_baseline = datetime.strptime(games[0]["time_begin"].split()[0], "%Y-%m-%d")

    field_map = {}
    field_id = 1
    for g in games:
        if g["field"] not in field_map:
            field_map[g["field"]] = field_id
            field_id += 1

    game_start = []
    game_end = []
    difficulty = []
    game_field = []

    for g in games:
        game_start.append(time_to_minutes(g["time_begin"], time_baseline))
        game_end.append(time_to_minutes(g["time_end"], time_baseline))
        difficulty.append(g["level_factor"])
        game_field.append(field_map[g["field"]])

    main_exp = []
    assist_exp = []
    available_slots = []


    for r in referees:
        main_exp.append(r["main_referee_experience"])
        assist_exp.append(r["assistant_referee_experience"])
        slots = []
        for slot in r["available_slots"]:
            from_min = time_to_minutes(slot["from"], time_baseline)
            to_min = time_to_minutes(slot["to"], time_baseline)
            slots.append((from_min, to_min))
        available_slots.append(slots)

    lines = []
    lines.append(f"NumGames = {len(games)};")
    lines.append(f"NumReferees = {len(referees)};")
    lines.append(f"NumFields = {len(field_map)};")

    lines.append(f"game_start = [{', '.join(map(str, game_start))}];")
    lines.append(f"game_end = [{', '.join(map(str, game_end))}];")
    lines.append(f"difficulty = [{', '.join(map(str, difficulty))}];")
    lines.append(f"game_field = [{', '.join(map(str, game_field))}];")
    lines.append(f"main_exp = [{', '.join(map(str, main_exp))}];")
    lines.append(f"assist_exp = [{', '.join(map(str, assist_exp))}];")

    lines.append("available_slots = array3d(1..NumReferees, 1..10, 1..2,[")
    for slots in available_slots:
        slot_strs = [f"{s[0]},{s[1]}" for s in slots]
        padded = slot_strs + ["0,0"] * (10 - len(slot_strs))  # pad to fixed width if needed
        lines.append("  " + ", ".join(padded) + ",")
    lines.append("]);")

    return "\n".join(lines)

# Usage
if __name__ == "__main__":
    with open("./data/sample.json", "r") as f:
        data = json.load(f)
    
    dzn_text = generate_dzn(data)
    with open("./data/dzn/sample.dzn", "w") as f:
        f.write(dzn_text)
    print(dzn_text)

    import minizinc
    
    # Load the MiniZinc model
    model = minizinc.Model("./scheduler.mzn")
    
    # Use Gecode solver
    gecode = minizinc.Solver.lookup("chuffed")
    
    # Create an instance and load data
    instance = minizinc.Instance(gecode, model)
    instance.add_file("./data/dzn/sample.dzn")
    
    # Solve
    result = instance.solve()
    print("✅ Solution:")
    print(result)
    
    
