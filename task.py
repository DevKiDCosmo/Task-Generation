import json
import os


def ask(prompt, default=None):
    """
    Prompt the user for input with an optional default value.
    """
    if default:
        prompt = f"{prompt} (default: {default}): "
    else:
        prompt = f"{prompt}: "
    
    response = input(prompt).strip()
    return response if response else default


def load_existing_task(file_path):
    """
    Load the existing task structure from a JSON file.
    """
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading existing file: {e}")
        return {}


def create_task_structure():
    """
    Interactively create or modify a task structure by asking the user for input.
    """
    task_structure = {}

    # Ask for the task ID
    task_id = ask("Enter the task ID (e.g., n1, n4)")
    if not task_id:
        print("Error: Task ID cannot be empty.")
        return None

    # Check if the file already exists
    output_dir = "./exercise"
    output_file = os.path.join(output_dir, f"{task_id}.json")
    if os.path.exists(output_file):
        modify = ask(f"The file '{task_id}.json' already exists. Do you want to modify it? (yes/no)", default="no").lower()
        if modify == "yes":
            task_structure = load_existing_task(output_file)
        else:
            print(f"Skipping task creation for '{task_id}'.")
            return None

    while True:
        # Ask for language
        language = ask("Enter the language (e.g., de, en, fr)").strip()
        if not language:
            print("Error: Language cannot be empty. Please try again.")
            continue

        # Check if the language is already used
        if language in task_structure:
            # Ask for version
            version = ask(f"Enter the version for {language} (e.g., 1.0)").strip()
            if not version:
                print("Error: Version cannot be empty. Please try again.")
                continue

            # Check if the version is already used for the language
            if version in task_structure[language]:
                overwrite = ask(f"The version '{version}' for language '{language}' already exists. Do you want to overwrite it? (yes/no)", default="no").lower()
                if overwrite != "yes":
                    print(f"Skipping version '{version}' for language '{language}'.")
                    continue
        else:
            # If the language is not used, ask for version
            version = ask(f"Enter the version for {language} (e.g., 1.0)").strip()
            if not version:
                print("Error: Version cannot be empty. Please try again.")
                continue

        # Ask for file paths
        paths = ask(f"Enter the file paths for {language} version {version} (comma-separated)").strip().split(",")
        paths = [path.strip() for path in paths if path.strip()]  # Remove leading/trailing spaces and empty strings

        # Remove duplicates
        paths = list(set(paths))

        if not paths:
            print("Error: File paths cannot be empty. Please try again.")
            continue

        # Add to the task structure
        if language not in task_structure:
            task_structure[language] = {}
        task_structure[language][version] = paths

        # Ask if the user wants to add more entries
        add_more = ask("Do you want to add more entries? (yes/no)", default="no").lower()
        if add_more != "yes":
            break

    return task_id, task_structure


def save_task_structure(task_id, task_structure):
    """
    Save the task structure to a JSON file.
    """
    # Ensure the output directory exists
    output_dir = "./exercise"
    os.makedirs(output_dir, exist_ok=True)

    # Save the task structure to a JSON file
    output_file = os.path.join(output_dir, f"{task_id}.json")
    with open(output_file, 'w', encoding="utf-8") as f:
        json.dump(task_structure, f, indent=4, ensure_ascii=False)

    print(f"Task structure saved successfully to {output_file}")


def main():
    # Create or modify the task structure interactively
    task_data = create_task_structure()
    if task_data is None:
        return

    task_id, task_structure = task_data

    # Save the task structure
    save_task_structure(task_id, task_structure)


if __name__ == "__main__":
    main()