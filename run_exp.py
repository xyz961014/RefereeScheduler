from minizinc_solve import minizinc_solve
from llm_solve import llm_solve
from pathlib import Path
import ipdb

def main():
    data_dir = Path("./data")
    for data_file in data_dir.iterdir():
        if data_file.suffix == ".json" and data_file.name.startswith("202"):
            #minizinc_solve(data_file, timeout=10)
            #minizinc_solve(data_file, timeout=60)
            #minizinc_solve(data_file, timeout=120)
            llm_solve(data_file, model="o3", reasoning_effort="medium")

if __name__ == "__main__":
    main()
