import os
docs_path = os.path.join(os.path.dirname(__file__), "readme.md")

def read():
    with open(docs_path,"r") as f:
        print(f.read())