import datetime
import json
import os
import sys
import uuid

from conda.env.env import from_file

# TODO: High priority changing everything since new version of exercise hirachic order.

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

    # Interactive input for form fields
    form_filename = ask("Enter the filename for the form (e.g., 'n1.json')", "n1.json")
    id_ = ask("Enter the ID of the exercise (e.g., 'No.1')", "No.1")
    category_ = ask("Enter the categories (comma-separated, e.g., 'Shoumei')", "Induction,Sums")
    cid = ask("Enter the CID (e.g., 'SH-1')", "SH-1")
    time = int(ask("Enter the time in minutes (e.g., '5')", "5"))
    nam_score = float(ask("Enter the name score (e.g., '1.0')", "1.0"))
    author = ask("Enter the author", "Original")
    difficulty = int(ask("Enter the difficulty (e.g., '1')", "1"))
    tags = ask("Enter the tags (comma-separated, e.g., 'Induction,Sums')", "Induction,Sums")

    form_filename = "/exercise/" +  form_filename + ".json"

    # Create JSON data
    form_data = {
        "id": id_,
        "category": [cat.strip() for cat in category_.split(",")],
        "cid": cid,
        "time": time,
        "nam_score": nam_score,
        "author": author,
        "date": datetime.datetime.now().strftime("%d.%m.%Y"),  # Current date
        "UUID": create_uuid(),
        "GUID": create_uuid(),
        "main": {
            "title": "Prove that $n^2 = \\sum^{{n}{2}}_{n = 1} = (2n - 1) = n^2$",
            "content": content,
            "solution": solution
        },
        "difficulty": difficulty,
        "tags": [tag.strip() for tag in tags.split(",")]
    }

    # Write JSON file
    with open(form_filename, "w", encoding="utf-8") as f:
        json.dump(form_data, f, ensure_ascii=False, indent=2)
    print(f"Form successfully created: {form_filename}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python exercise.py <content_path> <solution_path>")
        sys.exit(1)

    content_path = sys.argv[1]
    solution_path = sys.argv[2]
    create_form(content_path, solution_path)
