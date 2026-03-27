import os
import json

REMOVE_USER = os.getenv("REMOVE_USER")

def main():
    with open("reviewers.json","r") as f:
        reviewers = json.load(f)
    min_val = min([val for val in reviewers.values()])
    try:
        with open("tmp.json","r") as f:
            reviwers = json.load(f)
    except:
        pass
    reviewers[REMOVE_USER] = min_val
    with open("tmp.json","w") as f:
        json.dump(reviewers,f,indent=2)

if __name__ == "__main__":
    main()