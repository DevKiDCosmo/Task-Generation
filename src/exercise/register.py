import os
import json

def list_json_files(directory='./exercise', recursive=False):
    json_files = []
    if recursive:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    json_files.append(os.path.join(root, file))
    else:
        for file in os.listdir(directory):
            if file.endswith('.json'):
                json_files.append(os.path.join(directory, file))
    return json_files

def read_guids_and_uuids(json_files):
    guids_and_uuids = []
    for file in json_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                guid = data.get("GUID")
                uuid = data.get("UUID")
                if guid and uuid:
                    guids_and_uuids.append({"file": file, "GUID": guid, "UUID": uuid})
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Fehler beim Lesen der Datei {file}: {e}")
    return guids_and_uuids

def write_to_file(output_file, guids_and_uuids):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(guids_and_uuids, f, indent=4, ensure_ascii=False)
        print(f"GUIDs und UUIDs wurden erfolgreich in '{output_file}' geschrieben.")
    except Exception as e:
        print(f"Fehler beim Schreiben in die Datei: {e}")

def main():
    directory = './exercise'
    output_file = './guids_and_uuids.json'

    # Alle JSON-Dateien im gesamten Verzeichnis
    all_json_files = list_json_files(directory, recursive=True)

    # GUIDs und UUIDs auslesen
    guids_and_uuids = read_guids_and_uuids(all_json_files)

    # Ergebnisse in eine Datei schreiben
    write_to_file(output_file, guids_and_uuids)

if __name__ == "__main__":
    main()