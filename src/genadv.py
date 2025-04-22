import shutil
import string
import subprocess
import sys
import json
import os
import typing
import log as lg

exercise_dir = "./exercise/"
exerciseForProcessing = []
difficulty = "information/difficulty.json"  # Information about difficulty and translation
paths_exercise, paths_solution = [], []

log = lg.Log()


def phrase_exercise(information: typing.Dict) -> typing.Optional[None]:
    global exerciseForProcessing

    # Collect keys to remove
    keys_to_remove = []

    for information_access, content in list(information.items()):  # Use list() to safely iterate
        # Try to access the keys in the content dictionary
        try:
            languages_info = content["language"]
            version_info = content["version"]
            exercise_info = content["exercise"]
        except KeyError as e:
            log.write(f"KeyError: {e} in {information_access}")
            keys_to_remove.append(information_access)
            continue

        # Reading JSON file
        try:
            with open(f"./exercise/{information_access}.json", 'r', encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            log.write(f"JSONDecodeError: {information_access}.json is not a valid JSON file")
            keys_to_remove.append(information_access)
            continue
        except PermissionError:
            log.write(f"PermissionError: {information_access}.json is not accessible")
            keys_to_remove.append(information_access)
            continue
        except FileNotFoundError:
            log.write(f"FileNotFoundError: {information_access}.json not found in exercise folder")
            keys_to_remove.append(information_access)
            continue

        # Getting available languages from the data
        language_available = list(data.keys())

        # Check if lengths of language and version match
        if len(languages_info) != len(version_info):
            log.write(f"Error: Mismatched lengths for 'language' and 'version' in {information_access}. Skipping.")
            keys_to_remove.append(information_access)
            continue

        for language, version in zip(languages_info, version_info):
            if language not in language_available:
                log.write(f"Language {language} is not available in {information_access}")
                continue

            # Check if version is available for the language
            language_keys = list(data[language].keys())
            if len(language_keys) > 0:  # Ensure there is at least one key
                if version not in language_keys:  # Check if the version matches the key name
                    log.write(f"Version {version} is not available in {information_access} for {language}")
                    continue
            else:
                log.write(f"No keys available in {information_access} for {language}")
                continue

            # Process exercise_info globally for all languages and versions
            max_index = len(data[language][version])
            filtered_exercise_info = [i - 1 for i in exercise_info if 1 <= i <= max_index]

            if filtered_exercise_info:  # Ensure filtered_exercise_info is not empty
                for i in filtered_exercise_info:
                    try:
                        # Get the file name from the JSON data
                        file_name = data[language][version][i]
                        current = os.path.join(exercise_dir, file_name + ".json")
                        raw = os.path.join(exercise_dir, information_access)  # Give id not file_name

                        if os.path.exists(current):
                            exerciseForProcessing.append(
                                (language, current, version, raw))  # Append the correct version
                        else:
                            log.write(f"File does not exist: {current} in {information_access} for {language}")
                    except IndexError:
                        log.write(f"Index {i} is out of bounds in {information_access}")
            else:
                log.write(f"No valid exercise information available in {information_access} for {language}")

    # Remove invalid keys after iteration
    for key in keys_to_remove:
        del information[key]

    # Sort the exerciseForProcessing list by language
    exerciseForProcessing.sort(key=lambda x: (x[0], x[1]))

    # log.write(exerciseForProcessing)
    return None  # Isn't necessary, but added for clarity


def difficulty_to_str(difficulty_: int, language: str) -> str:
    global difficulty
    with open(difficulty, 'r', encoding="utf-8") as f:
        data = json.load(f)

    if language in data:
        # Convert difficulty_ to a string because JSON keys are strings
        difficulty_key = str(difficulty_)
        if difficulty_key in data[language]:
            return data[language][difficulty_key]
        else:
            return "Unknown Difficulty"
    else:
        return "Unknown Language"


def generating_exercise(language: string, file: string, paper: string, version: string, raw: string) -> None:
    global exerciseForProcessing
    with open(file, 'r', encoding="utf-8") as f:
        data = json.load(f)
        f.close()
    try:
        id_exercise = data["id"]
        category = data["category"]
        cid = data["cid"]
        time: int = data["time"]

        time: str = f"{time // 60} h {time % 60} min" if time >= 60 else f"{time} min"

        score = data["nam_score"]
        author = data["author"]
        date = data["date"]
        uuid = data["UUID"]
        guid = data["GUID"]
        difficulty_info: str = difficulty_to_str(data["difficulty"], language)
        tags = data["tags"]
    except KeyError as e:
        log.write(f"KeyError: {e} in {file}")
        return None
    except json.JSONDecodeError:
        log.write(f"JSONDecodeError: {file} is not a valid JSON file")
        return None
    except PermissionError:
        log.write(f"PermissionError: {file} is not accessible")
        return None

    # Generate dir
    if not os.path.exists(f"./generated/exercise/{language}"):
        os.makedirs(f"./generated/exercise/{language}")
    if not os.path.exists(f"./generated/exercise/{language}/{id_exercise}"):
        os.makedirs(f"./generated/exercise/{language}/{id_exercise}")
    if not os.path.exists(f"./generated/solution/{language}"):
        os.makedirs(f"./generated/solution/{language}")
    if not os.path.exists(f"./generated/solution/{language}/{id_exercise}"):
        os.makedirs(f"./generated/solution/{language}/{id_exercise}")

    # Split the main field into title, content, and solution
    main_content = data["main"]
    title = main_content.get("title", "Unknown Title")
    content = str(main_content.get("content", ""))
    solution = str(main_content.get("solution", ""))

    exercise_title = f"\\subsection{{{{{language.upper()} {cid} {id_exercise}{paper}V{version}}}: {title}}}\n"
    header_information = f"\\textbf{{Time for Exercise}}: {time} \\quad \\textit{{Nam-Score: {score}}} \\quad"

    with open(f"./generated/exercise/{language}/{id_exercise}/{paper}_{id_exercise}_{language}.tex", 'w',
              encoding="utf-8") as f:
        f.write(exercise_title)
        f.write(header_information)

        if author == "Original":
            f.write("\\textit{An Original}\n\n")
        else:
            f.write(f"\\textit{{Author: {author}}}\n\n")

        try:
            with open(path := raw + "/" +os.path.join(language, version, content), 'r', encoding="utf-8") as content_file:
                content_lines = content_file.read().splitlines()
                for line in content_lines:
                    f.write(line + "\n")
        except FileNotFoundError:
            log.write(f"FileNotFoundError: {path} not found")
            return None

        f.write(f"\n\\textbf{{Category}}: {', '.join(category)}\n")
        f.write(f"\\textbf{{Difficulty}}: {difficulty_info}\n")
        f.write(f"\\textbf{{Tags}}: {', '.join(tags)}\n\n")
        f.write(f"\\textbf{{UUID}}: {uuid}~--~\\textit{{GUID}}: {guid} on {date}\n")
    log.write(
        f"Generated exercise file: ./generated/exercise/{language}/{id_exercise}/{paper}_{id_exercise}_{language}.tex")

    with open(f"./generated/solution/{language}/{id_exercise}/{paper}_{id_exercise}_{language}.tex", 'w',
              encoding="utf-8") as f:
        f.write(exercise_title)
        f.write(header_information)

        if author == "Original":
            f.write("\\textit{An Original}\n\n")
        else:
            f.write(f"\\textit{{Author: {author}}}\n\n")

        try:
            with open(path := raw + "/" + os.path.join(language, version, content), 'r', encoding="utf-8") as content_file:
                content_lines = content_file.read().splitlines()
                for line in content_lines:
                    f.write(line + "\n")
        except FileNotFoundError:
            log.write(f"FileNotFoundError: {path} not found")
            return None

        f.write("\\hline\n")
        f.write("\\subsubsection{Solution}\n")

        try:
            with open(path := raw + "/" + os.path.join(language, version, solution), 'r', encoding="utf-8") as solution_file:
                solution_file = solution_file.read().splitlines()
                for line in solution_file:
                    f.write(line + "\n")
        except FileNotFoundError:
            log.write(f"FileNotFoundError: {path} not found")
            return None

        f.write(f"\n\\textbf{{Category}}: {', '.join(category)}\n")
        f.write(f"\\textbf{{Difficulty}}: {difficulty_info}\n")
        f.write(f"\\textbf{{Tags}}: {', '.join(tags)}\n\n")
        f.write(f"\\textbf{{UUID}}: {uuid}~--~\\textit{{GUID}}: {guid} on {date}\n")
    log.write(
        f"Generated solution file: ./generated/solution/{language}/{id_exercise}/{paper}_{id_exercise}_{language}.tex")

    paths_exercise.append(f"../exercise/{language}/{id_exercise}/{paper}_{id_exercise}_{language}")
    paths_solution.append(f"../solution/{language}/{id_exercise}/{paper}_{id_exercise}_{language}")

    return None


def copy_template(paper: string) -> None:
    # Check if the directory exists before attempting to copy
    if not os.path.exists("./template"):
        log.write("No 'template' directory to copy from.")
        return

    # Ensure the destination directory exists
    destination_dir = f"./generated/{paper}"
    os.makedirs(destination_dir, exist_ok=True)

    # Copy only banko.cls and template.tex
    files_to_copy = ["banko.cls", "template.tex"]
    for file_name in files_to_copy:
        source_path = os.path.join("./template", file_name)
        destination_path = os.path.join(destination_dir, file_name)
        if os.path.exists(source_path):
            shutil.copy2(source_path, destination_path)
        else:
            log.write(f"File {file_name} not found in the template directory.")

    # Rename template.tex to paper.tex
    template_path = os.path.join(destination_dir, "template.tex")
    new_path = os.path.join(destination_dir, f"{paper}.tex")
    if os.path.exists(template_path):
        os.rename(template_path, new_path)
    log.write(f"Copied and renamed template files to {destination_dir}.")


def compile_files(paper: string) -> None:
    # Change dir
    file = f"{paper}.tex"
    log.write(f"Generating PDF for file: {file}")
    os.chdir("./generated/" + paper)
    subprocess.run(
        ["xelatex.exe", "--shell-escape", "-synctex=1", "-interaction=nonstopmode", file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    log.write("Finishing init PDF")
    subprocess.run(
        ["xelatex.exe", "--shell-escape", "-synctex=1", "-interaction=nonstopmode", file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    log.write("Finishing content")
    subprocess.run(
        ["xelatex.exe", "--shell-escape", "-synctex=1", "-interaction=nonstopmode", file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    log.write("Finishing references and alignments")
    os.chdir("../..")
    log.write("PDF generation finished for file: " + file)


def generating_paper(paper: string, information: list) -> None:
    global exerciseForProcessing
    copy_template(paper)

    # Read the template file as a single string
    with open(f"./generated/{paper}/{paper}.tex", 'r', encoding="utf-8") as f:
        data = f.read()

    # Processing __PARAMETERS__ in the template
    # [title, date, paper, description, version, revision, archive, doi, tags]
    data = data.replace("__PAPER_TITLE__", information[0])
    data = data.replace("__PAPER_DATE__", information[1])
    data = data.replace("__PAPER_ID__", information[2])
    data = data.replace("__PAPER_DESCRIPTION__", information[3])
    data = data.replace("__PAPER_VERSION__", information[4])
    data = data.replace("__PAPER_REVISION__", information[5])
    data = data.replace("__PAPER_ARCHIVE__", information[6])
    data = data.replace("__PAPER_DOI__", information[7])
    data = data.replace("__PAPER_TAGS__", ' '.join(information[8]))

    import_list = ""
    for i in range(len(exerciseForProcessing)):
        import_list += f"\\input{{{paths_exercise[i]}}}\\clearpage\n"

    data = data.replace("__PAPER_IMPORTS__", import_list)

    # Extract all unique IDs from the exerciseForProcessing list
    used_ids = {os.path.basename(path).split('_')[1] for path in paths_exercise}

    # Join the IDs into a single string separated by commas
    import_list_id = ', '.join(sorted(used_ids))

    # Replace the placeholder with the generated list of IDs
    data = data.replace("__PAPER_USED_ID__", import_list_id)

    # Write the modified content back to the file
    with open(f"./generated/{paper}/{paper}.tex", 'w', encoding="utf-8") as f:
        f.write(data)
    compile_files(paper)
    log.write(f"Generated paper file: ./generated/{paper}/{paper}.tex")

    return None


def generating_solution_paper(paper: string, information: list) -> None:
    global exerciseForProcessing
    path = "solution" + paper
    copy_template(path)

    # Read the template file as a single string
    with open(f"./generated/{path}/{path}.tex", 'r', encoding="utf-8") as f:
        data = f.read()

    # Processing __PARAMETERS__ in the template
    # [title, date, paper, description, version, revision, archive, doi, tags]
    data = data.replace("__PAPER_TITLE__", information[0])
    data = data.replace("__PAPER_DATE__", information[1])
    data = data.replace("__PAPER_ID__", information[2])
    data = data.replace("__PAPER_DESCRIPTION__", information[3])
    data = data.replace("__PAPER_VERSION__", information[4])
    data = data.replace("__PAPER_REVISION__", information[5])
    data = data.replace("__PAPER_ARCHIVE__", information[6])
    data = data.replace("__PAPER_DOI__", information[7])
    data = data.replace("__PAPER_TAGS__", ' '.join(information[8]))

    import_list = ""
    for i in range(len(exerciseForProcessing)):
        import_list += f"\\input{{{paths_exercise[i]}}}\\clearpage\n"
    for i in range(len(exerciseForProcessing)):
        import_list += f"\\input{{{paths_solution[i]}}}\\clearpage\n"
    data = data.replace("__PAPER_IMPORTS__", import_list)

    # Extract all unique IDs from the exerciseForProcessing list
    used_ids = {os.path.basename(path).split('_')[1] for path in paths_exercise}

    # Join the IDs into a single string separated by commas
    import_list_id = ', '.join(sorted(used_ids))

    # Replace the placeholder with the generated list of IDs
    data = data.replace("__PAPER_USED_ID__", import_list_id)

    # Write the modified content back to the file
    with open(f"./generated/{path}/{path}.tex", 'w', encoding="utf-8") as f:
        f.write(data)
    compile_files(path)
    log.write(f"Generated paper file: ./generated/{path}/{path}.tex")

    return None


def clear_absolute():  # Not used for bucket creation
    """
    Remove everything in the 'generated' folder.
    """
    try:
        if os.path.exists("./generated"):
            shutil.rmtree("./generated")
            log.write("Removed 'generated' directory and its contents.")
        else:
            log.write("No 'generated' directory to remove.")
    except Exception as e:
        log.write(f"Error while clearing 'generated' directory: {e}")


def clear_non_pdf():
    # Check if the directory exists
    if not os.path.exists("./generated"):
        log.write("No 'generated' directory to clean.")
        return

    # Walk through the directory
    for root, dirs, files in os.walk("./generated", topdown=False):
        for file in files:
            if not file.endswith(".pdf"):  # Keep only PDF files
                os.remove(os.path.join(root, file))
                log.write(f"Removed file: {os.path.join(root, file)}")
        for dir_ in dirs:
            dir_path = os.path.join(root, dir_)
            # Remove directories if they are empty
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                log.write(f"Removed empty directory: {dir_path}")

    log.write("Cleaned 'generated' directory, keeping only PDF files.")


def main(file: string) -> None:
    clear_non_pdf()
    try:
        with open(file, 'r', encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        log.write(f"JSONDecodeError: {file} is not a valid JSON file")
        return None
    except PermissionError:
        log.write(f"PermissionError: {file} is not accessible")
        return None
    except FileNotFoundError:
        log.write(f"FileNotFoundError: {file} not found")
        return None

    log.write("Generating paper from JSON file")

    title = data["title"]
    date = data["date"]
    paper = data["paper"]
    description = data["description"]
    version = data["version"]
    revision = data["revision"]
    archive = data["archive"]
    doi = data["doi"]
    tags = data["tags"]
    exercise = data["exercise"]

    phrase_exercise(exercise)

    for language, file, version, raw in exerciseForProcessing:
        generating_exercise(language, file, paper, version, raw)

    generating_paper(paper, [title, date, paper, description, version, revision, archive, doi, tags])
    generating_solution_paper(paper, [title, date, paper, description, version, revision, archive, doi, tags])

    clear_non_pdf()
    log.create_log()


if __name__ == "__main__":
    main(sys.argv[1])
