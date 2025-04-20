import os
import json
from datetime import datetime

def create_paper_json():
    # Prompt the user for input
    paperid = input("Enter the paper ID (e.g., P1.0): ").strip()
    title = input(f"Enter the title for {paperid} (default: 'Paper {paperid}'): ").strip() or f"Paper {paperid}"
    description = input("Enter the description of the paper: ").strip() or "This is a description of the paper."
    version = input("Enter the version (default: 1.0): ").strip() or "1.0"
    revision = input("Enter the revision (default: 1): ").strip() or "1"
    archive = input(f"Enter the archive name (default: {paperid}-archive): ").strip() or f"{paperid}-archive"
    doi = input("Enter the DOI (optional): ").strip()
    tags = input("Enter tags (comma-separated, e.g., example,paper,template): ").strip().split(",") or ["example", "paper", "template"]

    # Prompt for exercise information
    exercise_data = {}
    while True:
        exercise_id = input("Enter the exercise ID (e.g., n1, n4): ").strip()
        languages = input(f"Enter the languages for {exercise_id} (comma-separated, e.g., de,en,fr): ").strip().split(",")
        versions = input(f"Enter the versions for {exercise_id} (comma-separated, matching the languages): ").strip().split(",")
        exercises = input(f"Enter exercise numbers for {exercise_id} (comma-separated): ").strip().split(",")
        
        # Ensure the lengths of languages and versions match
        if len(languages) != len(versions):
            print("Error: The number of languages and versions must match. Please try again.")
            continue

        # Add the exercise data
        exercise_data[exercise_id] = {
            "language": [lang.strip() for lang in languages if lang.strip()],
            "version": [ver.strip() for ver in versions if ver.strip()],
            "exercise": [int(ex.strip()) for ex in exercises if ex.strip()]
        }

        # Ask if the user wants to add more exercises
        continue_prompt = input("Do you want to add more exercises? (yes/no): ").strip().lower()
        if continue_prompt != "yes":
            break

    # Define the structure of the paper.json
    paper_data = {
        "title": title,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "paper": paperid,
        "description": description,
        "version": version,
        "revision": revision,
        "archive": archive,
        "doi": doi,
        "tags": [tag.strip() for tag in tags if tag.strip()],
        "exercise": exercise_data
    }

    # Ensure the output directory exists
    output_dir = "./generated"
    os.makedirs(output_dir, exist_ok=True)

    # Write the JSON file
    output_file = os.path.join(output_dir, f"{paperid}.json")
    with open(output_file, 'w', encoding="utf-8") as f:
        json.dump(paper_data, f, indent=4, ensure_ascii=False)

    print(f"Created {output_file}")

def main():
    create_paper_json()

if __name__ == "__main__":
    main()