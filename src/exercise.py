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

    path = f"{exercise_id}/{language}/{version}/{exercise_id}-{language}"
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


def create_exercise_structure(base_dir, exercise_id, language, version, metadata, shared_uuid):
    exercise_path = os.path.join(base_dir, exercise_id, language, version)
    os.makedirs(exercise_path, exist_ok=True)

    for sub in ["content", "solution"]:
        os.makedirs(os.path.join(exercise_path, sub), exist_ok=True)

    metadata["UUID"] = shared_uuid
    metadata["GUID"] = str(uuid.uuid4())

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


def main():
    print("Übungsstruktur-Generator")

    base_dir = input("Basisverzeichnis (z.B. './exercise') [Standard: './exercise']: ").strip() or './exercise'
    exercise_id = input("Übungs-ID [Standard: 'default_id']: ").strip() or 'default_id'
    language = input("Sprache (z.B. 'de', 'en', 'jp') [Standard: 'en']: ").strip() or 'en'
    version = input("Version (z.B. '1.0') [Standard: '1.0']: ").strip() or '1.0'

    categories = {
        1: "Shoemei",
        2: "Kaiketsu und Toku",
        3: "Bunseki",
        4: "Keisan",
        5: "Kochiku und Sekkei",
        6: "Kaishaku"
    }

    category_input = input("Kategorie (Komma-getrennt, z.B. '2,3,1,5') [Standard: '1,2']: ").strip() or '1,2'
    c = input("Nummer für CID: ")

    category_numbers = [int(c) for c in category_input.split(",")]
    if len(category_numbers) == 1:
        cid = f"{categories[category_numbers[0]][0]}{categories[category_numbers[0]][1]}"
    else:
        if category_numbers[1] == 5:
            cid = f"{categories[category_numbers[0]][0]}{categories[category_numbers[0]][1]}KS"
        else:
            cid = f"{categories[category_numbers[0]][0]}{categories[category_numbers[0]][1]}{categories[category_numbers[1]][0]}"
    cid = (cid.upper() + "-" + str(c)).upper()

    time = input("Zeit (in Minuten, z.B. '2700') [Standard: '60']: ").strip() or '60'
    nam_score = input("NAM-Score (z.B. '7.5') [Standard: '5.0']: ").strip() or '5.0'
    author = input("Autor [Standard: 'Original']: ").strip() or 'Original'
    date = input(f"Datum (z.B. 'DD.MM.YYYY') [Standard: '{datetime.date.today().strftime('%d.%m.%Y')}']: ").strip() or datetime.date.today().strftime("%d.%m.%Y")
    title = input("Titel [Standard: 'Default Title']: ").strip() or 'Default Title'
    difficulty = input("Schwierigkeitsgrad (z.B. '6') [Standard: '1']: ").strip() or '1'
    tags = input("Tags (Komma-getrennt, z.B. 'tag1,tag2') [Standard: '']: ").strip() or ''

    register_file = os.path.join(base_dir, f"{exercise_id}.json")
    if os.path.exists(register_file):
        with open(register_file, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
                shared_uuid = existing_data.get("UUID", str(uuid.uuid4()))
            except json.JSONDecodeError:
                shared_uuid = str(uuid.uuid4())
    else:
        shared_uuid = str(uuid.uuid4())

    is_subtask = input("Ist dies eine Teilaufgabe? (ja/nein) [Standard: 'nein']: ").strip().lower() == "ja"
    parent_id = input("ID der Hauptaufgabe: ").strip() if is_subtask else None

    # Remove from exercise_id the first char
    id_ = exercise_id[1:]

    metadata = {
        "id": f"No.{id_}",
        "category": [int(c) for c in category_input.split(",")],
        "cid": cid,
        "time": int(time),
        "nam_score": float(nam_score),
        "author": author,
        "date": date,
        "main": {
            "title": title,
            "content": f'content/{exercise_id}-{language}.exr',
            "solution": f'solution/{exercise_id}-{language}.exr'
        },
        "difficulty": int(difficulty),
        "tags": tags.split(",") if tags else []
    }

    create_exercise_structure(base_dir, exercise_id, language, version, metadata, shared_uuid)
    create_or_update_register_file(base_dir, exercise_id, language, version, shared_uuid, parent_id)


if __name__ == "__main__":
    main()
