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

def write_combined_json(top_level_files, all_files, output_file):
    data = {
        "top": top_level_files,
        "all": all_files
    }
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    directory = './exercise'

    # JSON-Dateien im obersten Verzeichnis
    top_level_json_files = list_json_files(directory, recursive=False)

    # Alle JSON-Dateien im gesamten Verzeichnis
    all_json_files = list_json_files(directory, recursive=True)

    # Kombinierte JSON-Datei schreiben
    write_combined_json(top_level_json_files, all_json_files, './exercise/register.json')

    print("JSON-Dateien wurden erfolgreich registriert.")

if __name__ == "__main__":
    main()