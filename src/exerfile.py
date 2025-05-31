import os
import json
import uuid
import datetime

def load_batch_from_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def create_exercise_structure(base_dir, exercise_id, language, version, metadata, shared_uuid, subtask_id=None):
    lang_dir = os.path.join(base_dir, language)
    version_dir = os.path.join(lang_dir, version)
    content_dir = os.path.join(version_dir, "content")
    solution_dir = os.path.join(version_dir, "solution")
    metadata_dir = os.path.join(version_dir, "metadata")

    os.makedirs(content_dir, exist_ok=True)
    os.makedirs(solution_dir, exist_ok=True)
    os.makedirs(metadata_dir, exist_ok=True)

    suffix = f"-{subtask_id}" if subtask_id else ""
    content_path = os.path.join(content_dir, f"{exercise_id}{suffix}-{language}.exr")
    solution_path = os.path.join(solution_dir, f"{exercise_id}{suffix}-{language}.exr")
    metadata_path = os.path.join(metadata_dir, f"{exercise_id}{suffix}-{language}.json")

    # Leere Inhalte anlegen
    if not os.path.exists(content_path):
        with open(content_path, "w", encoding="utf-8") as f:
            f.write("")
    if not os.path.exists(solution_path):
        with open(solution_path, "w", encoding="utf-8") as f:
            f.write("")

    # Metadaten schreiben
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

def create_or_update_register_file(base_dir, exercise_id, language, version, shared_uuid, subtask_id=None):
    register_path = os.path.join(base_dir, f"{exercise_id}.json")
    entry = {
        "lang": language,
        "version": version,
        "uuid": shared_uuid
    }
    if subtask_id:
        entry["id"] = subtask_id

    data = {}
    if os.path.exists(register_path):
        try:
            with open(register_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    key = f"{language}-{version}-{subtask_id}" if subtask_id else f"{language}-{version}"
    data[key] = entry

    with open(register_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def main():
    print("Stapelverarbeitung von Aufgaben aus JSON-Datei")
    json_path = input("Pfad zur JSON-Datei: ").strip()
    data = load_batch_from_json(json_path)

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
        with open(register_file, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
                shared_uuid = existing_data.get("UUID", str(uuid.uuid4()))
            except json.JSONDecodeError:
                shared_uuid = str(uuid.uuid4())
    else:
        shared_uuid = str(uuid.uuid4())

    for i, lang in enumerate(languages):
        for version in versions:
            if partial:
                for pid in partial_ids:
                    exercise_id_ = f"{exercise_id}-{pid}"
                    title = titles.get(str(pid), ["Default Title"] * len(languages))[i] if str(pid) in titles else "Default Title"
                    time = times[pid % len(times)] if times else 60
                    metadata = {
                        "id": f"No.{exercise_id_}",
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
                    create_exercise_structure(base_dir, exercise_id, lang, version, metadata, shared_uuid, str(pid))
                    create_or_update_register_file(base_dir, exercise_id, lang, version, shared_uuid, str(pid))
            else:
                title = titles.get("1", ["Default Title"] * len(languages))[i] if "1" in titles else "Default Title"
                time = times[0] if times else 60
                metadata = {
                    "id": f"No.{exercise_id}",
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
                create_exercise_structure(base_dir, exercise_id, lang, version, metadata, shared_uuid, None)
                create_or_update_register_file(base_dir, exercise_id, lang, version, shared_uuid, None)

if __name__ == "__main__":
    main()
