import shutil
import string
import subprocess
import sys
import json
import os

ids = []


def generate_exercise(file_id: string, paper_id: string):
    global ids
    # Verzeichnisse nur einmal erstellen
    try:
        os.makedirs("./generated/raw/exercise", exist_ok=True)
        os.makedirs("./generated/raw/solution", exist_ok=True)
    except OSError as e:
        print(f"Fehler beim Erstellen der Verzeichnisse: {e}")
        return None

    with open(f"./exercise/{file_id}.json", 'r', encoding="utf-8") as f:
        data = json.load(f)

    id = data["id"]
    category = data["category"]
    cid = data["cid"]
    languages = data["languages"]
    difficulty = data["difficulty"]
    tags = data["tags"]
    time = data["time"]

    # Format Time min (int) -> _ h _ min (str)
    time = f"{time // 60} h {time % 60} min" if time >= 60 else f"{time} min"

    version = data["version"]
    author = data["author"]
    nam_score = data["nam_score"]

    files, solutions = [], []
    for language, content in languages.items():
        filename = f"{paper_id}_{id}_{language}.tex"

        title = content["title"]
        exercise_content = content["content"]
        solution = content["solution"]
        code = content["code"]

        # Übungsdatei schreiben
        with open(f"./generated/raw/exercise/{filename}", 'w', encoding="utf-8") as f:
            f.write(f"\\subsection{{{{{code.upper()} {cid} {id}{paper_id}V{version}}}: {title}}}\n")

            f.write(f"\\textbf{{Time for Exercise}}: {time} \\quad \\textit{{Nam-Score: {nam_score}}} \\quad")

            if author == "Original":
                f.write("\\textit{An Original}\n\n")
            else:
                f.write(f"\\textit{{Author: {author}}}\n\n")

            for line in exercise_content:
                f.write(line + "\n")
            f.write(f"\n\\textbf{{Category}}: {', '.join(category)}\n")
            f.write(f"\\textbf{{Difficulty}}: {difficulty}\n")
            f.write(f"\\textbf{{Tags}}: {', '.join(tags)}\n")
        print("Generated exercise file:", filename)

        # Lösungsdatei schreiben
        with open(f"./generated/raw/solution/{filename}", 'w', encoding="utf-8") as f:
            f.write(f"\\subsection{{{{{code.upper()} {cid} {id}{paper_id}V{version}}}: {title}}}\n")

            f.write(f"\\textbf{{Time for Exercise}}: {time} \\quad \\textit{{Nam-Score: {nam_score}}} \\quad")

            if author == "Original":
                f.write("\\textit{An Original}\n\n")
            else:
                f.write(f"\\textit{{Author: {author}}}\n\n")

            for line in exercise_content:
                f.write(line + "\n")

            f.write("\\vspace{1em}\\hrule\\vspace{1em}\n")

            f.write(f"\\subsubsection{{Solution for SOL-{code.upper()} {cid} {id}{paper_id}V{version}}}\n")
            for line in solution:
                f.write(line + "\n")
            f.write(f"\n\\textbf{{Category}}: {', '.join(category)}\n\n")
            f.write(f"\\textbf{{Difficulty}}: {difficulty}\n\n")
            f.write(f"\\textbf{{Tags}}: {', '.join(tags)}\n\n")
        print("Generated solution file:", filename)

        files.append(f"./raw/exercise/{filename}")
        solutions.append(f"./raw/solution/{filename}")
        ids.append(f"{code.upper()} {cid} {id}{paper_id}V{version}")
        ids.append(f"SOL-{code.upper()} {cid} {id}{paper_id}V{version}")

    return files, solutions


def compile_files(file: string) -> None:
    # Change dir
    print("Generating PDF for file:", file)
    os.chdir("./generated")
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
    os.chdir("..")
    print("PDF generation finished for file:", file)


def generate_paper(file_id: string, title, date, paper, description, version, revision, imports, tags, doi, archive) -> None:
    global ids
    # Read template. replace placeholders with data
    filename = file_id + ".tex"
    with open("template.tex", 'r', encoding="utf-8") as f:
        template = f.read()
        f.close()
    # Search for __PAPER_TITLE__, __PAPER_DATE__, __PAPER_ID__, __PAPER_DESCRIPTION__, __PAPER_VERSION__, __PAPER_REVISION__
    template = template.replace("__PAPER_TITLE__", title)
    template = template.replace("__PAPER_DATE__", date)
    template = template.replace("__PAPER_ID__", file_id)
    template = template.replace("__PAPER_DESCRIPTION__",
                                "Created automatically: " + description)
    template = template.replace("__PAPER_VERSION__", version)
    template = template.replace("__PAPER_REVISION__", revision)
    template = template.replace("__PAPER_USED_ID__", " ".join(ids))
    template = template.replace("__PAPER_TAGS__", ", ".join(tags))
    template = template.replace("__PAPER_DOI__", doi)
    template = template.replace("__PAPER_ARCHIVE__", archive)

    # __PAPER_IMPORTS__

    imports_str = ""
    for i in range(len(imports)):
        # Zuerst die Übungen einfügen
        for k in range(len(imports[i][0])):  # Übungen befinden sich im ersten Index
            imports_str += "\\include{" + str(imports[i][0][k]) + "}\n"  # Exercises

    # Danach die Lösungen einfügen
    for i in range(len(imports)):
        for k in range(len(imports[i][1])):  # Lösungen befinden sich im zweiten Index
            imports_str += "\\include{" + str(imports[i][1][k]) + "} % Solution \n"  # Solutions

    template = template.replace("__PAPER_IMPORTS__", imports_str)

    try:
        os.makedirs("./generated")
    except FileExistsError:
        pass
    except OSError:
        print("Error creating directory")
        return None

    with open("./generated/solution_" + filename, 'w', encoding="utf-8") as f:
        f.write(template)
        f.close()
    print("Generated file: solution_", filename)
    compile_files("solution_" + filename)

    with open("./generated/" + filename, 'w', encoding="utf-8") as f:
        template = "\n".join([line for line in template.splitlines() if "% Solution" not in line])
        f.write(template)
        f.close()
    print("Generated file:", filename)
    compile_files(filename)

    return None

def clear_files():
    # Entferne alle Dateien und Verzeichnisse im Ordner 'generated', außer Dateien mit der Endung '.cls'
    for filename in os.listdir("./generated"):
        file_path = os.path.join("./generated", filename)
        if os.path.isfile(file_path) and not filename.endswith(".cls"):
            os.remove(file_path)
            print("Removed file:", filename)
        elif os.path.isdir(file_path) and not filename.endswith(".cls"):
            shutil.rmtree(file_path)
            print("Removed directory:", filename)

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
    exercise = data["exercise"]
    tags = data["tags"]
    doi = data["doi"]
    archive = data["archive"]

    imports = []

    for i in range(len(exercise)):
        imports.append(generate_exercise(exercise[i], paper))

    generate_paper(paper, title, date, paper, description, version, revision, imports, tags, doi, archive)


if __name__ == "__main__":
    main(sys.argv[1])
