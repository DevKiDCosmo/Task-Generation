import shutil
import string
import subprocess
import sys
import json
import os
import typing

exercise_dir = "./exercise/"
exerciseProcess = []
difficulty = "information/difficulty.json"
paths_exercise, paths_solution = [], []

def prase_exercise(information: typing.Dict) -> typing.Optional[None]:
    global exerciseProcess
    
    # Collect keys to remove
    keys_to_remove = []

    for infomration_access, content in list(information.items()):  # Use list() to safely iterate
        # Try to access the keys in the content dictionary
        try:
            languages_info = content["language"]
            version_info = content["version"]
            exercise_info = content["exercise"]
        except KeyError as e:
            print(f"KeyError: {e} in {infomration_access}")
            keys_to_remove.append(infomration_access)
            continue

        # Reading JSON file
        try:
            with open(f"./exercise/{infomration_access}.json", 'r', encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"JSONDecodeError: {infomration_access}.json is not a valid JSON file")
            keys_to_remove.append(infomration_access)
            continue
        except PermissionError:
            print(f"PermissionError: {infomration_access}.json is not accessible")
            keys_to_remove.append(infomration_access)
            continue
        except FileNotFoundError:
            print(f"FileNotFoundError: {infomration_access}.json not found in exercise folder")
            keys_to_remove.append(infomration_access)
            continue

        # Getting available languages from the data
        language_avaiable = list(data.keys())

        # Check if lengths of language and version match
        if len(languages_info) != len(version_info):
            print(f"Error: Mismatched lengths for 'language' and 'version' in {infomration_access}. Skipping.")
            keys_to_remove.append(infomration_access)
            continue

        for language, version in zip(languages_info, version_info):
            if language not in language_avaiable:
                print(f"Language {language} is not available in {infomration_access}")
                continue

            # Check if version is available for the language
            language_keys = list(data[language].keys())
            if len(language_keys) > 0:  # Ensure there is at least one key
                if version not in language_keys:  # Check if the version matches the key name
                    print(f"Version {version} is not available in {infomration_access} for {language}")
                    continue
            else:
                print(f"No keys available in {infomration_access} for {language}")
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

                        if os.path.exists(current):
                            exerciseProcess.append((language, current, version))  # Append the correct version
                        else:
                            print(f"File does not exist: {current} in {infomration_access} for {language}")
                    except IndexError:
                        print(f"Index {i} is out of bounds in {infomration_access}")
            else:
                print(f"No valid exercise information available in {infomration_access} for {language}")

    # Remove invalid keys after iteration
    for key in keys_to_remove:
        del information[key]

    # Sort the exerciseProcess list by language
    exerciseProcess.sort(key=lambda x: (x[0], x[1]))

    # print(exerciseProcess)
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


def generating_exercise(language: string, file: string, paper: string, version: string) -> None:
    global exerciseProcess
    with open(file, 'r', encoding="utf-8") as f:
        data = json.load(f)
        f.close()
    try:
        id = data["id"]
        category = data["category"]
        cid = data["cid"]
        time: int = data["time"]
        
        time: str = f"{time // 60} h {time % 60} min" if time >= 60 else f"{time} min"
        
        score = data["nam_score"]
        author = data["author"]
        date = data["date"]
        UUID = data["UUID"]
        GUID = data["GUID"]
        difficulty: str = difficulty_to_str(data["difficulty"], language)
        tags = data["tags"]
    except KeyError as e:
        print(f"KeyError: {e} in {file}")
        return None
    except json.JSONDecodeError:
        print(f"JSONDecodeError: {file} is not a valid JSON file")
        return None
    except PermissionError:
        print(f"PermissionError: {file} is not accessible")
        return None
    
    # Generate dir
    if not os.path.exists(f"./generated/exercise/{language}"):
        os.makedirs(f"./generated/exercise/{language}")
    if not os.path.exists(f"./generated/exercise/{language}/{id}"):
        os.makedirs(f"./generated/exercise/{language}/{id}")
    if not os.path.exists(f"./generated/solution/{language}"):
        os.makedirs(f"./generated/solution/{language}")
    if not os.path.exists(f"./generated/solution/{language}/{id}"):
        os.makedirs(f"./generated/solution/{language}/{id}")
     
    # Split the main field into title, content, and solution
    main = data["main"]
    title = main.get("title", "Unknown Title")
    content = main.get("content", [])
    solution = main.get("solution", [])

   
    with open(f"./generated/exercise/{language}/{id}/{paper}_{id}_{language}.tex", 'w', encoding="utf-8") as f:
        f.write(f"\\subsection{{{{{language.upper()} {cid} {id}{paper}V{version}}}: {title}}}\n")

        f.write(f"\\textbf{{Time for Exercise}}: {time} \\quad \\textit{{Nam-Score: {score}}} \\quad")

        if author == "Original":
            f.write("\\textit{An Original}\n\n")
        else:
            f.write(f"\\textit{{Author: {author}}}\n\n")

        for line in content:
            f.write(line + "\n")
        f.write(f"\n\\textbf{{Category}}: {', '.join(category)}\n")
        f.write(f"\\textbf{{Difficulty}}: {difficulty}\n")
        f.write(f"\\textbf{{Tags}}: {', '.join(tags)}\n\n")
        f.write(f"\\textbf{{UUID}}: {UUID}~--~\\textit{{GUID}}: {GUID} on {date}\n")
    print("Generated exercise file:", f"./generated/exercise/{language}/{id}/{paper}_{id}_{language}.tex")
    
    with open(f"./generated/solution/{language}/{id}/{paper}_{id}_{language}.tex", 'w', encoding="utf-8") as f:
        f.write(f"\\subsection{{{{{language.upper()} {cid} {id}{paper}V{version}}}: {title}}}\n")

        f.write(f"\\textbf{{Time for Exercise}}: {time} \\quad \\textit{{Nam-Score: {score}}} \\quad")

        if author == "Original":
            f.write("\\textit{An Original}\n\n")
        else:
            f.write(f"\\textit{{Author: {author}}}\n\n")

        for line in content:
            f.write(line + "\n")
        
        f.write("\\hline\n")
        f.write("\\subsubsection{Solution}\n")
            
        for line in solution:
            f.write(line + "\n")
            
        f.write(f"\n\\textbf{{Category}}: {', '.join(category)}\n")
        f.write(f"\\textbf{{Difficulty}}: {difficulty}\n")
        f.write(f"\\textbf{{Tags}}: {', '.join(tags)}\n\n")
        f.write(f"\\textbf{{UUID}}: {UUID}~--~\\textit{{GUID}}: {GUID} on {date}\n")
    print("Generated solution file:", f"./generated/solution/{language}/{id}/{paper}_{id}_{language}.tex")
    
    paths_exercise.append(f"../exercise/{language}/{id}/{paper}_{id}_{language}")
    paths_solution.append(f"../solution/{language}/{id}/{paper}_{id}_{language}")
    
    return None

def copy_template(paper: string) -> None:
    # Check if the directory exists before attempting to copy
    if not os.path.exists("./template"):
        print("No 'template' directory to copy from.")
        return

    # Copy the template directory to the generated folder
    shutil.copytree("./template", f"./generated/{paper}", dirs_exist_ok=True)
    
    # Rename template.tex to paper.tex
    template_path = f"./generated/{paper}/template.tex"
    new_path = f"./generated/{paper}/{paper}.tex"
    if os.path.exists(template_path):
        os.rename(template_path, new_path)
    print("Copied template files to generated folder.")

def compile_files(paper: string) -> None:
    # Change dir
    file = f"{paper}.tex"
    print("Generating PDF for file:", file)
    os.chdir("./generated/" + paper)
    subprocess.run(
        ["xelatex.exe", "--shell-escape", "-synctex=1", "-interaction=nonstopmode", file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("Finishing init PDF")
    subprocess.run(
        ["xelatex.exe", "--shell-escape", "-synctex=1", "-interaction=nonstopmode", file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("Finishing content")
    subprocess.run(
        ["xelatex.exe", "--shell-escape", "-synctex=1", "-interaction=nonstopmode", file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("Finishing references and alignments")
    os.chdir("../..")
    print("PDF generation finished for file:", file)

def generating_paper(paper: string, information: list) -> None:
    global exerciseProcess
    copy_template(paper)
    
    # Read the template file as a single string
    with open(f"./generated/{paper}/{paper}.tex", 'r', encoding="utf-8") as f:
        data = f.read()  # Use read() instead of readlines()
    
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
    for i in range(len(exerciseProcess)):
        import_list += f"\\input{{{paths_exercise[i]}}}\\clearpage\n"
        
    data = data.replace("__PAPER_IMPORTS__", import_list)
    
    # Extract all unique IDs from the exerciseProcess list
    used_ids = {os.path.basename(path).split('_')[1] for path in paths_exercise}
    
    # Join the IDs into a single string separated by commas
    import_list_id = ', '.join(sorted(used_ids))
    
    # Replace the placeholder with the generated list of IDs
    data = data.replace("__PAPER_USED_ID__", import_list_id)
    
    
    # Write the modified content back to the file
    with open(f"./generated/{paper}/{paper}.tex", 'w', encoding="utf-8") as f:
        f.write(data)
    compile_files(paper)
    print("Generated paper file:", f"./generated/{paper}/{paper}.tex")
    
    return None

def generating_solution_paper(paper: string, information: list) -> None:
    global exerciseProcess
    path = "solution" + paper
    copy_template(path)
    
    # Read the template file as a single string
    with open(f"./generated/{path}/{path}.tex", 'r', encoding="utf-8") as f:
        data = f.read()  # Use read() instead of readlines()
    
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
    for i in range(len(exerciseProcess)):
        import_list += f"\\input{{{paths_exercise[i]}}}\\clearpage\n"
    for i in range(len(exerciseProcess)):
        import_list += f"\\input{{{paths_solution[i]}}}\\clearpage\n"
    data = data.replace("__PAPER_IMPORTS__", import_list)
    
    # Extract all unique IDs from the exerciseProcess list
    used_ids = {os.path.basename(path).split('_')[1] for path in paths_exercise}
    
    # Join the IDs into a single string separated by commas
    import_list_id = ', '.join(sorted(used_ids))
    
    # Replace the placeholder with the generated list of IDs
    data = data.replace("__PAPER_USED_ID__", import_list_id)
    
    
    # Write the modified content back to the file
    with open(f"./generated/{path}/{path}.tex", 'w', encoding="utf-8") as f:
        f.write(data)
    compile_files(path)
    print("Generated paper file:", f"./generated/{path}/{path}.tex")
    
    return None

def clear_files():
    # Check if the directory exists before attempting to clear it
    if not os.path.exists("./generated"):
        print("No 'generated' directory to clear.")
        return

    # Remove the entire 'generated' directory
    shutil.rmtree("./generated")
    print("Removed 'generated' directory and all its contents.")

def main(file: string) -> None:
    clear_files()
    with open(file, 'r', encoding="utf-8") as f:
        data = json.load(f)

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

    prase_exercise(exercise)
    
    for language, file, version in exerciseProcess:
        generating_exercise(language, file, paper, version)

    generating_paper(paper, [title, date, paper, description, version, revision, archive, doi, tags])
    generating_solution_paper(paper, [title, date, paper, description, version, revision, archive, doi, tags])

if __name__ == "__main__":
    main(sys.argv[1])