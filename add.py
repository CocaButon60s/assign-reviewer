import os
import json

ADD_USER = os.getenv("ADD_USER")

def main():
    with open("reviewers.json","r") as f:
        reviewers = json.load(f)
    max_val = max([val for val in reviewers.values()])
    try:
        with open("tmp.json","r") as f:
            reviwers = json.load(f)
    except:
        pass
    reviewers[ADD_USER] = max_val
    with open("tmp.json","w") as f:
        json.dump(reviewers,f,indent=2)

if __name__ == "__main__":
    main()