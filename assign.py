import os
import json
import numpy as np
import requests

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ASSIGN_COUNT = int(os.environ["ASSIGN_COUNT"])
DECAY_RATE = float(os.environ["DECAY_RATE"])

PR_NUMBER = os.environ["PR_NUMBER"]
REPO = os.environ["REPO"]
AUTHOR = os.environ["AUTHOR"]


def select_reviewers():
    with open("reviewers.json", "r") as f:
        default = json.load(f)
    try:
        with open("tmp.json", "r") as f:
            now = json.load(f)
    except:
        now = default.copy()

    reviewers = {k: float(v) for k, v in now.items() if k != AUTHOR}
    ret = []
    while len(ret) < ASSIGN_COUNT:
        names = list(reviewers.keys())
        weights = list(reviewers.values())
        reviewer = np.random.choice(names, p=np.array(weights) / sum(weights))
        now[reviewer] += (default[reviewer] - now[reviewer]) * DECAY_RATE
        ret.append(str(reviewer))
        reviewers = {k: float(v) for k, v in reviewers.items() if k != reviewer}

    with open("tmp.json", "w") as f:
        json.dump(now, f, indent=2)

    return ret


def main():
    reviewers = select_reviewers()
    print("Selected reviewers:", reviewers)

    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/requested_reviewers"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    data = {"reviewers": reviewers}

    response = requests.post(url, headers=headers, json=data)
    print(response.status_code, response.text)


if __name__ == "__main__":
    main()
