import os
import json
import uuid
import datetime


def create_or_update_register_file(base_dir, exercise_id, language, version, shared_uuid, parent_id=None):
    register_file = os.path.join(base_dir, f"{exercise_id}.json")
    existing_data = {}

    if os.path.exists(register_file):
        with open(register_file, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                print(f"Fehler beim Lesen der Datei {register_file}. Die Datei wird überschrieben.")

    shared_uuid = existing_data.get("UUID", shared_uuid)

    if language not in existing_data:
        existing_data[language] = {}
    if version not in existing_data[language]:
        existing_data[language][version] = []

    if parent_id is not None:
        exercise_id_ = f"{exercise_id}-{parent_id}"
    else:
        exercise_id_ = exercise_id

    path = f"{exercise_id}/{language}/{version}/{exercise_id_}-{language}"
    if path not in existing_data[language][version]:
        existing_data[language][version].append(path)

    existing_data["UUID"] = shared_uuid

    with open(register_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

    print(f"Registerdatei '{register_file}' wurde erfolgreich erstellt oder aktualisiert.")

    if parent_id:
        parent_file = os.path.join(base_dir, f"{parent_id}.json")
        if os.path.exists(parent_file):
            with open(parent_file, "r", encoding="utf-8") as f:
                try:
                    parent_data = json.load(f)
                except json.JSONDecodeError:
                    print(f"Fehler beim Lesen der Datei {parent_file}.")
                    return

            if "subtasks" not in parent_data:
                parent_data["subtasks"] = []
            if exercise_id not in parent_data["subtasks"]:
                parent_data["subtasks"].append(exercise_id)

            with open(parent_file, "w", encoding="utf-8") as f:
                json.dump(parent_data, f, indent=4, ensure_ascii=False)

            print(f"Teilaufgabe '{exercise_id}' wurde in der Hauptaufgabe '{parent_id}' registriert.")


def create_exercise_structure(base_dir, exercise_id, language, version, metadata, shared_uuid, parent_id):
    exercise_path = os.path.join(base_dir, exercise_id, language, version)
    os.makedirs(exercise_path, exist_ok=True)

    for sub in ["content", "solution"]:
        os.makedirs(os.path.join(exercise_path, sub), exist_ok=True)

    metadata["UUID"] = shared_uuid
    metadata["GUID"] = str(uuid.uuid4())

    if parent_id is not None:
        exercise_id += "-" + parent_id

    metadata_file = f"{exercise_id}-{language}.json"
    with open(os.path.join(exercise_path, metadata_file), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    content_path = os.path.join(exercise_path, "content", f"{exercise_id}-{language}.exr")
    solution_path = os.path.join(exercise_path, "solution", f"{exercise_id}-{language}.exr")

    with open(content_path, "w", encoding="utf-8") as f:
        f.write(f"Content for {exercise_id} in {language}")

    with open(solution_path, "w", encoding="utf-8") as f:
        f.write(f"Solution for {exercise_id} in {language}")

    print(f"Struktur und Dateien für '{exercise_id}' in Sprache '{language}' wurden erfolgreich erstellt.")


def prepare_metadata_items(data):
    base_dir = data.get("Base", "./exercise")
    exercise_id = data.get("ID", "default_id")
    versions = data.get("Version", ["1.0"])
    languages = data.get("Language", ["en"])
    categories = data.get("Category", [1])
    cid = str(data.get("CID", "1"))
    times = data.get("Time", [60])
    nam_score = float(data.get("NAM-Score", 5.0))
    author = data.get("Author", "Original")
    date = data.get("Date", datetime.date.today().strftime("%d.%m.%Y"))
    difficulty = int(data.get("Difficulty", 1))
    tags = data.get("Tags", [])
    partial = data.get("Partial", False)
    partial_ids = data.get("ID_partial", [1])
    titles = data.get("Title", {})

    register_file = os.path.join(base_dir, f"{exercise_id}.json")
    if os.path.exists(register_file):
        try:
            with open(register_file, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                shared_uuid = existing_data.get("UUID", str(uuid.uuid4()))
        except json.JSONDecodeError:
            shared_uuid = str(uuid.uuid4())
    else:
        shared_uuid = str(uuid.uuid4())

    metadata_items = []

    for i, lang in enumerate(languages):
        for version in versions:
            if partial:
                for pid in partial_ids:
                    exercise_id_ = f"{exercise_id}-{pid}"
                    title = titles.get(str(pid), ["Default Title"] * len(languages))[i] if str(
                        pid) in titles else "Default Title"
                    time = times[pid % len(times)] if times else 60

                    # Remove any alphabetic characters from exercise_id
                    exercise_id_cleaned = ''.join(filter(str.isdigit, exercise_id_))

                    # Entferne alle numerischen Zeichen aus exercise_id
                    type_of_exercise = ''.join(filter(str.isalpha, exercise_id_)).lower()

                    if type_of_exercise == "n":
                        type_of_exercise = "No."
                    elif type_of_exercise == "m":
                        type_of_exercise = "Masterclass Exercise."

                    metadata = {
                        "id": f"{type_of_exercise} {exercise_id_cleaned}",
                        "category": categories,
                        "cid": cid,
                        "time": time,
                        "nam_score": nam_score,
                        "author": author,
                        "date": date,
                        "main": {
                            "title": title,
                            "content": f'content/{exercise_id_}-{lang}.exr',
                            "solution": f'solution/{exercise_id_}-{lang}.exr'
                        },
                        "difficulty": difficulty,
                        "tags": tags
                    }
                    metadata_items.append((base_dir, exercise_id, lang, version, metadata, shared_uuid, str(pid)))
            else:
                title = titles.get("1", ["Default Title"] * len(languages))[i] if "1" in titles else "Default Title"
                time = times[0] if times else 60

                # Remove any alphabetic characters from exercise_id
                exercise_id_cleaned = ''.join(filter(str.isdigit, exercise_id))

                # Entferne alle numerischen Zeichen aus exercise_id
                type_of_exercise = ''.join(filter(str.isalpha, exercise_id)).lower()

                if type_of_exercise == "n":
                    type_of_exercise = "No."
                elif type_of_exercise == "m":
                    type_of_exercise = "Masterclass Exercise."

                metadata = {
                    "id": f"{type_of_exercise} {exercise_id_cleaned}",
                    "category": categories,
                    "cid": cid,
                    "time": time,
                    "nam_score": nam_score,
                    "author": author,
                    "date": date,
                    "main": {
                        "title": title,
                        "content": f'content/{exercise_id}-{lang}.exr',
                        "solution": f'solution/{exercise_id}-{lang}.exr'
                    },
                    "difficulty": difficulty,
                    "tags": tags
                }
                metadata_items.append((base_dir, exercise_id, lang, version, metadata, shared_uuid, None))

    return metadata_items

def load_batch_from_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def main():
    print("Stapelverarbeitung von Aufgaben aus JSON-Datei")
    json_path = input("Pfad zur JSON-Datei: ").strip()
    data = load_batch_from_json(json_path)

    metadata_items = prepare_metadata_items(data)

    for item in metadata_items:
        base_dir, exercise_id, lang, version, metadata, shared_uuid, subtask_id = item
        create_exercise_structure(base_dir, exercise_id, lang, version, metadata, shared_uuid, subtask_id)
        create_or_update_register_file(base_dir, exercise_id, lang, version, shared_uuid, subtask_id)



if __name__ == "__main__":
    main()
