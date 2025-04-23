import datetime
import json
import os
import sys
import uuid

from conda.env.env import from_file

# TODO: High priority changing everything since new version of exercise hirachic order.
# WARNING: This is a work in progress and not all features are implemented yet.
# Practical trash code


# exercise/id/language/version/
# - content/
# - solution/
# - json

def create_uuid():
    return str(uuid.uuid4())

def ask(prompt, default=None):
    if default:
        prompt = f"{prompt} (default: {default}): "
    else:
        prompt = f"{prompt}: "

    response = input(prompt).strip()
    return response if response else default


def create_form(pathC, pathS):
    # Check if the files exist
    if not os.path.exists(pathC):
        print(f"Error: The file {pathC} does not exist.")
        return
    if not os.path.exists(pathS):
        print(f"Error: The file {pathS} does not exist.")
        return

    # Read the contents of the files
    with open(pathC, 'r', encoding='utf-8') as content_file:
        content = content_file.read().splitlines()

    with open(pathS, 'r', encoding='utf-8') as solution_file:
        solution = solution_file.read().splitlines()

    # Check if the contents are empty
    if not content:
        print(f"Error: The file {pathC} is empty.")
        return
    if not solution:
        print(f"Error: The file {pathS} is empty.")
        return

    # Ask

    # Template
    form = {
        "id": "No.1",
        "category": ["Shoemei"],
        "cid": "SH-1",
        "time": 5,
        "nam_score": 1.0,
        "author": "Original",
        "date": "19.04.2025",
        "UUID": create_uuid(),
        "GUID": create_uuid(),
        "main": {
            "title": "Beweise, dass $n^2 = \\sum^{{n}{2}}_{n = 1} = (2n - 1) = n^2$",
            "content": "content/n1-de.exr",
            "solution": "solution/n1-de.exr"
        },
        "difficulty": 1,
        "tags": ["Induktion", "Summen", "Ungerade Zahlen", "Naturelle Zahlen"]
    }



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python exercise.py <content_path> <solution_path>")
        sys.exit(1)

    content_path = sys.argv[1]
    solution_path = sys.argv[2]
    create_form(content_path, solution_path)
