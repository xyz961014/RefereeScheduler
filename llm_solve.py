from pathlib import Path
import json
from openai import OpenAI
import os
import ipdb
from pprint import pprint
import time

from evaluation import validate_and_score

openai_api_key = os.getenv("OPENAI_API_KEY")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

def llm_solve(data_path, model="o3", reasoning_effort="medium"):
    """
    Sends a structured prompt to the OpenAI LLM to assign referees to football games
    based on availability, experience, and fairness constraints.
    """
    data_path = Path(data_path)
    with open(data_path, "r") as f:
        data = json.load(f)
    

    # Create the prompt to explain the assignment task
    prompt = f"""
You are a constraint reasoning assistant. Given a list of football games and a list of referees, assign referees to games according to the rules below.

Each game needs:
- 1 main referee
- 2 assistant referees
- 1 fourth official

Constraints:
- No referee can participate in overlapping matches.
- A referee can only be assigned as main/assistant referee to at most 2 games total (fatigue constraint).
- All assignments must be within the referee's available time slots.
- A referee can only serve one role per game.
- If a referee is assigned to two games on different fields, there must be at least 30 minutes between the end of the first and the start of the next.
- Try to assign more experienced referees to difficult matches.
- The fourth official does not need experience and is not affected by fatigue.

Return the result as a JSON list of assignments in the following format:

[
  {{
    "game_id": <game_id>,
    "main_referee": <ref_id>,
    "assistant_referees": [<ref_id1>, <ref_id2>],
    "fourth_official": <ref_id>
  }},
  ...
]

Only return the JSON, no explanation.

Here is the data:

```json
{json.dumps(data, indent=2)}
'''
"""
    if model.startswith("deepseek"):
        client = OpenAI(api_key=deepseek_api_key,
                        base_url="https://api.deepseek.com")
    else:
        client = OpenAI(api_key=openai_api_key)
    # Call OpenAI Chat API
    #print(prompt)
    time_start = time.time()
    response = client.chat.completions.create(
        model=model,
        reasoning_effort=reasoning_effort,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    # Extract and parse JSON result
    content = response.choices[0].message.content.strip()
    time_used = time.time() - time_start
    print("{} {} Solution: (time used: {:.2f}s)".format(
            model,
            reasoning_effort,
            time_used)
        )
    print(content)

    try:
        content = content.replace("```", "").strip()
        json_start = content.find("[")
        assignments = json.loads(content[json_start:])

        eval_res = validate_and_score(data, assignments)
        eval_res["time"] = time_used

        print("=" * 80)
        print("✅ {} {} {} Solution: (time used: {:.2f}s)".format(
                data_path.stem,
                model,
                reasoning_effort,
                time_used)
            )
        pprint(eval_res)
        print("Mean Score: {:.2f}".format(eval_res["score"] / eval_res["num_games"]))
        print("=" * 80)
        return eval_res
    except Exception as e:
        print(f"Failed to parse LLM response:\n{content}\n Error: {e}") 
        assignments = []
        eval_res = validate_and_score(data, assignments)
        eval_res["time"] = time_used
    finally:
        # Save result
        with open(f"./results/{data_path.stem}_{model}_{reasoning_effort}.json", "w") as f:
            json.dump(assignments, f, indent=4)

        with open(f"./results/{data_path.stem}_{model}_{reasoning_effort}_eval.json", "w") as f:
            json.dump(eval_res, f, indent=4)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, 
                        default="./data/sample.json",
                        help="input data")
    parser.add_argument("--model", type=str, 
                        default="o4-mini",
                        help="model")
    parser.add_argument("--reasoning_effort", type=str, 
                        default="medium",
                        choices=["low", "medium", "high"],
                        help="input data")
    args = parser.parse_args()

    llm_solve(args.data, model=args.model, reasoning_effort=args.reasoning_effort)
