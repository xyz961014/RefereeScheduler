import argparse
from pathlib import Path
import json
import minizinc
import time
from datetime import timedelta

from json_to_dzn import generate_dzn

import ipdb


def main(args):
    data_path = Path(args.data)
    dzn_path = Path(f"./data/dzn/{data_path.stem}.dzn")

    with open(data_path, "r") as f:
        data = json.load(f)
    
    dzn_text = generate_dzn(data)
    print(dzn_text)

    with open(dzn_path, "w") as f:
        f.write(dzn_text)

    # Load the MiniZinc model
    model = minizinc.Model("./scheduler.mzn")
    
    # Use Chuffed solver
    chuffed = minizinc.Solver.lookup("chuffed")
    
    # Create an instance and load data
    instance = minizinc.Instance(chuffed, model)
    instance.add_file(dzn_path)
    
    # Solve
    time_start = time.time()
    result = instance.solve(timeout=timedelta(seconds=args.timeout))
    print("✅ Solution: (time used: {:.2f}s)".format(time.time() - time_start))
    print(result)
    if result.solution is None:
        return

    game_ids = instance["game_id"]
    referee_ids = instance["referee_id"]
    num_games = instance["NumGames"]
    assignments = []

    for i in range(num_games):
        game_id = game_ids[i]
        assignments.append({
            "game_id": game_id,
            "main_referee": referee_ids[int(result["main_ref"][i]) - 1],
            "assistant_referees": [
                referee_ids[int(result["assistant_ref"][i][0]) - 1],
                referee_ids[int(result["assistant_ref"][i][1]) - 1],
            ],
            "fourth_official": referee_ids[int(result["fourth_official"][i]) - 1],
        })
    #print(json.dumps(assignments, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, 
                        default="./data/sample.json",
                        help="input data")
    parser.add_argument("--timeout", type=int, default=60,
                        help="solver timeout")
    args = parser.parse_args()
    main(args)
