import argparse
from pathlib import Path
import json
import minizinc

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
    result = instance.solve()
    print("✅ Solution:")
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, 
                        default="./data/sample.json",
                        help="input data")
    args = parser.parse_args()
    main(args)
