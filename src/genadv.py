import shutil, sys, os
import subprocess
import typing, json
from typing import Any, Coroutine

from util import log as lg
# import mypy
import asyncio, aiofiles
from dotenv import load_dotenv
import datetime
import code_gen.code_16 as c16
import code_gen.code_256 as c256
import re
import tempfile
import uuid

log = lg.Log()


class Generation():
    def __init__(self, exerciseDIR: str, difficulty_: str, translation_: str, category_: str):
        self.exercise_dir = exerciseDIR
        self.difficulty = difficulty_
        self.translation = translation_
        self.category = category_
        self.language = ""
        self.exam = False
        self.version = "1.5.4-MDLS Release - with Markdown Compilation 1.3.2-Prerelease and LaTeX Syntax Checking 0.5Beta"
        self.sorted = True

    async def phrase_exercise(self, information: typing.Dict, exerciseForProcessing: list[tuple[str, str, str, str]]) -> \
            list[
                tuple[str, str, str, str]]:

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
                async with aiofiles.open(f"./exercise/{information_access}.json", 'r', encoding="utf-8") as f:
                    content = await f.read()  # Asynchrones Lesen der Datei
                    data = json.loads(content)  # JSON-Daten parsen
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

                # Check if a version is available for the language
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
        def extract_number(s):
            match = re.search(r'(?:No|Test)\.(\d+)', s)
            return int(match.group(1)) if match else 0

        # Fixing from No.10 No.9 to No.9 No.10.
        if self.sorted:
            exerciseForProcessing.sort(key=lambda x: (x[0], extract_number(x[1])))

        # log.write(exerciseForProcessing)
        return exerciseForProcessing

    async def validating_exercise(self, exercise: str, uuid: list[str], guid: list[str]) -> tuple[bool, str, str]:
        # Validate the JSON file
        try:
            async with aiofiles.open(exercise, 'r', encoding="utf-8") as f:
                content = await f.read()  # Asynchrones Lesen der Datei
                data_exercise = json.loads(content)  # JSON-Daten parsen
        except json.JSONDecodeError:
            log.write(f"JSONDecodeError: {exercise} is not a valid JSON file")
            return False, "", ""
        except PermissionError:
            log.write(f"PermissionError: {exercise} is not accessible")
            return False, "", ""
        except FileNotFoundError:
            log.write(f"FileNotFoundError: {exercise} not found in exercise folder")
            return False, "", ""

        exercise_id = exercise.replace(self.exercise_dir, "").split("/")[0].replace(".json", "")
        task_path = os.path.join(self.exercise_dir, exercise_id + ".json")

        # Read the task JSON file
        try:
            async with aiofiles.open(task_path, 'r', encoding="utf-8") as f:
                task_content = await f.read()
                data_task = json.loads(task_content)
        except (FileNotFoundError, json.JSONDecodeError):
            log.write(f"Error reading task file: {task_path}")
            return False, "", ""

        # Check if GUID is unique
        if data_exercise["GUID"] in guid:
            log.write(f"GUID {data_exercise['GUID']} is not unique in {exercise}")
            return False, "", ""

        # Check if UUID is unique to its task
        if data_exercise["UUID"] in uuid:
            if data_task["UUID"] != data_exercise["UUID"]:
                log.write(f"UUID {data_exercise['UUID']} is not unique to its exercise in {task_path} and {exercise}")
                return False, "", ""

        keys = ["id", "category", "cid", "time", "nam_score", "author", "date", "UUID", "GUID", "difficulty", "tags",
                "main"]
        main_keys = ["title", "content", "solution"]

        for key in keys:
            if key not in data_exercise:
                log.write(f"Key {key} not found in {exercise}")
                return False, "", ""
        for key in main_keys:
            if key not in data_exercise["main"]:
                log.write(f"Key {key} not found in {exercise}")
                return False, "", ""

        return True, data_exercise["UUID"], data_exercise["GUID"]

    def difficulty_to_str(self, difficulty_: int, language: str) -> str:
        with open(self.difficulty, 'r', encoding="utf-8") as f:
            data = json.load(f)

        if language in data:
            # Convert difficulty_ to a str because JSON keys are strs
            difficulty_key = str(difficulty_)
            if difficulty_key in data[language]:
                return data[language][difficulty_key]
            else:
                return "Unknown Difficulty"
        else:
            return "Unknown Language"

    def category_to_str(self, category_: int, language: str) -> str:
        with open(self.category, 'r', encoding="utf-8") as f:
            data = json.load(f)

        if language in data:
            key = str(category_)
            if key in data[language]:
                return data[language][key]
            else:
                return "Unknown Difficulty"
        else:
            return "Unknown Language"

    def translation_to_str(self, translation_key: str, language: str) -> str:
        try:
            with open(self.translation, 'r', encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            log.write(f"Error loading translation file: {e}")
            return "Unknown Translation"

        # Überprüfen, ob der Übersetzungsschlüssel existiert
        if translation_key in data:
            # Überprüfen, ob die Sprache existiert
            if language in data[translation_key]:
                return data[translation_key][language]
            else:
                return f"Unknown Language: {language}"
        else:
            return f"Unknown Translation for key: {translation_key}"

    def markdown_to_latex(self, lines: list[str]) -> list[str]:
        output = []
        stack: list[tuple[str, int]] = []
        previous_indent = 0
        last_was_list = False

        def close_to_indent(target_indent: int):
            while stack and stack[-1][1] >= target_indent:
                env, _ = stack.pop()
                output.append(f'\\end{{{env}}}')

        def apply_formatting(text: str) -> str:
            text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\\textbf{\\textit{\1}}', text)
            text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
            text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\\textit{\1}', text)
            text = re.sub(r'__(.+?)__', r'\\underline{\1}', text)
            text = re.sub(r'~~(.+?)~~', r'\\sout{\1}', text)
            text = re.sub(r'`([^`]+?)`', r'\\texttt{\1}', text)
            text = re.sub(r'^\s*#+\s+(.*)', r'\\subsubsection{\1}', text)
            return text

        i = 0
        while i < len(lines):
            raw_line = lines[i]
            line = raw_line.rstrip()
            indent = len(raw_line) - len(raw_line.lstrip(' '))
            content = line.strip()

            next_indent = 0
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                next_indent = len(next_line) - len(next_line.lstrip(' '))

            is_item = re.match(r'^(?<!#)-\s*(.*)', content)
            is_enum = re.match(r'^(?<!#)(\d+)\.\s+(.*)', content)

            if is_item or is_enum:
                kind = 'enumerate' if is_enum else 'itemize'

                # Neue verschachtelte Liste?
                if not stack or indent > stack[-1][1]:
                    output.append(f'\\begin{{{kind}}}')
                    stack.append((kind, indent))
                else:
                    # Vorherige schließen
                    close_to_indent(indent)
                    if not stack or stack[-1][0] != kind:
                        output.append(f'\\begin{{{kind}}}')
                        stack.append((kind, indent))

                if is_enum:
                    num, text = is_enum.groups()
                    output.append(rf'\item[{num}.] {apply_formatting(text)}')
                else:
                    text = is_item.group(1)
                    output.append(rf'\item {apply_formatting(text)}')
                last_was_list = True

            elif content == '' and last_was_list and next_indent > indent:
                # Leere Listenzeile, nächste ist eingerückt → neue geschachtelte Liste erwartet
                pass
            else:
                # Normaler Text oder leer
                close_to_indent(0)
                if content:
                    output.append(apply_formatting(content))
                last_was_list = False

            previous_indent = indent
            i += 1

        close_to_indent(0)
        return output

    # TODO: Absolute bad.
    async def checking_syntax(self, file: str) -> bool | tuple[None, None, str]:
        base_temp_dir = "./temp"
        os.makedirs(base_temp_dir, exist_ok=True)
        temp_dir = os.path.join(base_temp_dir, str(uuid.uuid4()))
        os.makedirs(temp_dir, exist_ok=True)

        temp_tex = os.path.join(temp_dir, "syntax_check.tex")
        banko_src = os.path.join("./template", "banko.cls")
        banko_dst = os.path.join(temp_dir, "banko.cls")

        log.write("Checking LaTeX syntax for file: " + temp_tex + ". From " + file)

        if not os.path.exists(banko_src):
            log.write(f"FileNotFoundError: {banko_src} not found")
            return False

        shutil.copy2(banko_src, banko_dst)

        try:
            async with aiofiles.open(temp_tex, "w", encoding="utf-8") as f:
                await f.write(
                    r"\documentclass{banko}" "\n")  # Banko is preferred - It has probably every package - Very powerful
                await f.write(r"\begin{document}" "\n")
                # Inhalt der Datei einfügen

                if file.startswith("../exercise"):
                    file = file.replace("../exercise", "./generated/exercise", 1)
                elif file.startswith("../solution"):
                    file = file.replace("../solution", "./generated/solution", 1)

                file += ".tex"

                async with aiofiles.open(file, "r", encoding="utf-8") as content_file:
                    async for line in content_file:
                        await f.write(line)

                await f.write(r"\end{document}" "\n")

            try:
                result = subprocess.run(
                    ["xelatex", "-no-pdf", "-file-line-error", "-interaction=nonstopmode",
                     temp_tex.replace("\\", "/").split("/")[-1]],
                    cwd=temp_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=15
                )
            except subprocess.TimeoutExpired:
                #subprocess.kill()
                return None, None, "Timeout expired"
            except Exception as e:
                return None, None, str(e)

            try:
                output = result.stdout.decode('utf-8') + result.stderr.decode('utf-8')
            except UnicodeDecodeError:
                output = result.stdout.decode('latin1') + result.stderr.decode('latin1')

            CRITICAL_ERROR_PATTERNS = {
                "E001": r"! LaTeX Error:",
                "E002": r"! Undefined control sequence\.",
                "E003": r"! Emergency stop\.",
                "E004": r"! Missing .* inserted\.",
                "E005": r"! File ended while scanning",
                "E006": r"! Too many \}'s\.",
                "E007": r"Fatal error occurred, no output PDF file produced!",
                "E009": r"! I can't write on file",
            }

            found_errors = []

            for code, pattern in CRITICAL_ERROR_PATTERNS.items():
                if code == "E008":
                    if not re.search(pattern, output):  # PDF output fehlt
                        found_errors.append((code, "No PDF output produced"))
                else:
                    matches = re.findall(pattern, output)
                    for match in matches:
                        found_errors.append((code, match))

            if found_errors:
                log.write(f"LaTeX syntax check failed. Origin: {file}. Code: {result.returncode}. Errors:\n")
                for code, msg in found_errors:
                    log.write(f"  {code}: {msg}\n")
                    print(f"{code}: {msg}")
                return False
            else:
                log.write("Finished LaTeX syntax check for file: " + temp_tex)
                return True

        except Exception as e:
            log.write(f"LaTeX-syntax checking went wrong: {e} from {file}")
            return False

    def generating_exercise(self, language: str, file: str, paper: str, version: str, raw: str,
                            paths_exercise: list, paths_solution: list) -> tuple[int, list[str], list[str]]:

        # Needs to be changed to async

        with open(file, 'r', encoding="utf-8") as f:
            data = json.load(f)
        try:
            id_exercise = data["id"]
            category = [self.category_to_str(i, language) for i in data["category"]]

            cid = data["cid"]
            time: int = data["time"]

            score = data["nam_score"]
            author = data["author"]
            date = data["date"]
            uuid = data["UUID"]
            guid = data["GUID"]

            time_str: str = f"{time // 60} h {time % 60} min" if time >= 60 else f"{time} min"
            difficulty_str: str = self.difficulty_to_str(data["difficulty"], language)

            tags = data["tags"]
        except KeyError as e:
            log.write(f"KeyError: {e} in {file}")
            return 0, [""], [""]
        except json.JSONDecodeError:
            log.write(f"JSONDecodeError: {file} is not a valid JSON file")
            return 0, [""], [""]
        except PermissionError:
            log.write(f"PermissionError: {file} is not accessible")
            return 0, [""], [""]

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
        header_information = f"\\textbf{{{self.translation_to_str("eta", language)}}}: {time_str} \\quad \\textit{{Nam-Score: {score}}} \\quad"

        author_info = f"\\textit{{{self.translation_to_str('original', language)}}}\n\n" if author == "Original" else f"\\textit{{{self.translation_to_str('author', language)}: {author}}}\n\n"

        try:
            with open(path := raw + "/" + os.path.join(language, version, content), 'r',
                      encoding="utf-8") as content_file:
                content_lines: list[str] = content_file.read().splitlines()
        except FileNotFoundError:
            log.write(f"FileNotFoundError: {path} not found")
            return (0, [""], [""])

        with open(f"./generated/exercise/{language}/{id_exercise}/{paper}_{id_exercise}_{language}.tex", 'w',
                  encoding="utf-8") as f:
            f.write(exercise_title)
            f.write(header_information)
            f.write(author_info)

            content_lines = self.markdown_to_latex(content_lines)
            for line in content_lines:
                f.write(line + "\n")

            f.write(f"\n\\textbf{{{self.translation_to_str("category", language)}}}: {', '.join(category)}\n")
            f.write(f"\\textbf{{{self.translation_to_str("difficulty", language)}}}: {difficulty_str}\n")
            f.write(f"\\textbf{{{self.translation_to_str("tags", language)}}}: {', '.join(tags)}\n\n")
            f.write(
                f"\\textbf{{UUID}}: {uuid}~--~\\textit{{GUID}}: {guid} {self.translation_to_str("on_date", language)} {date}\n")
        log.write(
            f"Generated exercise file: ./generated/exercise/{language}/{id_exercise}/{paper}_{id_exercise}_{language}.tex")

        with open(f"./generated/solution/{language}/{id_exercise}/{paper}_{id_exercise}_{language}.tex", 'w',
                  encoding="utf-8") as f:
            f.write(exercise_title)
            f.write(header_information)
            f.write(author_info)

            content_lines = self.markdown_to_latex(content_lines)
            for line in content_lines:
                f.write(line + "\n")

            # f.write("\\noindent\\rule{10cm}{0.4pt}\n")
            f.write("\\vspace{1cm}\n")
            f.write(f"\\subsubsection{{{self.translation_to_str("solution", language)}}}\n")

            try:
                with open(path := raw + "/" + os.path.join(language, version, solution), 'r',
                          encoding="utf-8") as content_:  # Change to content_ because mypy
                    solution_file: list[str] = content_.read().splitlines()

                    solution_lines = self.markdown_to_latex(solution_file)
                    for line in solution_lines:
                        f.write(line + "\n")
            except FileNotFoundError:
                log.write(f"FileNotFoundError: {path} not found")
                return (0, [""], [""])

            f.write(f"\n\\textbf{{{self.translation_to_str("category", language)}}}: {', '.join(category)}\n")
            f.write(f"\\textbf{{{self.translation_to_str("difficulty", language)}}}: {difficulty_str}\n")
            f.write(f"\\textbf{{{self.translation_to_str("tags", language)}}}: {', '.join(tags)}\n\n")
            f.write(
                f"\\textbf{{UUID}}: {uuid}~--~\\textit{{GUID}}: {guid} {self.translation_to_str("on_date", language)} {date}\n")
        log.write(
            f"Generated solution file: ./generated/solution/{language}/{id_exercise}/{paper}_{id_exercise}_{language}.tex")

        paths_exercise.append(f"../exercise/{language}/{id_exercise}/{paper}_{id_exercise}_{language}")
        paths_solution.append(f"../solution/{language}/{id_exercise}/{paper}_{id_exercise}_{language}")

        return data["time"], paths_exercise, paths_solution

    def instruction_translation(self, language: str) -> str:
        instruction_path = "translation/instruction_translation.json"
        try:
            with open(instruction_path, 'r', encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            log.write(f"Error loading instruction translation file: {e}")
            return "Unknown Instruction"

        if language in data:
            try:
                with open(f"./translation/{data[language]}", 'r', encoding="utf-8") as content:
                    return content.read()
            except (FileNotFoundError, PermissionError) as e:
                log.write(f"Error reading translation file for language '{language}': {e}")
                return "Unknown Instruction"
        else:
            return f"Instruction not available for language: {language}"

    def copy_template(self, paper: str) -> None:
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

        # Copy fonts

        fonts_dir = os.path.join("./template", "fonts")
        if os.path.exists(fonts_dir):
            destination_fonts_dir = os.path.join(destination_dir, "fonts")
            shutil.copytree(fonts_dir, destination_fonts_dir, dirs_exist_ok=True)

        # Rename template.tex to paper.tex
        template_path = os.path.join(destination_dir, "template.tex")
        new_path = os.path.join(destination_dir, f"{paper}.tex")
        if os.path.exists(template_path):
            os.rename(template_path, new_path)
        log.write(f"Copied and renamed template files to {destination_dir}.")

    async def compile_files(self, paper: str) -> None:
        # Generiere den Dateinamen
        file = f"{paper}.tex"
        log.write(f"Generating PDF for file: {file}")

        # Setze den Arbeitsordner für die Kompilierung
        working_dir = os.path.join("./generated", paper)

        # Führe die Kompilierung mit dem angegebenen Arbeitsordner aus
        for step in ["init PDF", "content", "references and alignments"]:
            process = await asyncio.create_subprocess_exec(
                "xelatex.exe", "--shell-escape", "-synctex=1", "-interaction=nonstopmode", file,
                cwd=working_dir,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            await process.communicate()
            log.write(f"Finishing {step} for file: {file}")

        log.write(f"PDF generation finished for file: {file}")

    def exercise_and_times(self, data: str, exerciseForProcessing: list[tuple[str, str, str, str, int]],
                           paths_exercise: list[str], solution: str = "") -> str:
        import_list = ""
        previous_language = None

        if self.exam:
            import_list += "\\input{../stamp/stamp}\n\n"

        previous_language_time = None
        list_TotalTime = {}
        for i, (language, _, _, _, time) in enumerate(exerciseForProcessing):
            # Initialisiere die Liste oder den Wert für die Sprache, falls nicht vorhanden
            if language not in list_TotalTime:
                list_TotalTime[language] = 0  # Initialisiere mit 0 für die Summierung

            # Addiere die Zeit für jede Sprache
            if language != previous_language_time:
                list_TotalTime[language] += time
            else:
                list_TotalTime[language] += time  # Zeit wird weiterhin addiert

        # Convert the times (min) into hours and minutes
        formatted_TotalTime: dict[str, str] = {}

        for language, time in list_TotalTime.items():
            if time >= 60:
                hours = time // 60
                minutes = time % 60
                formatted_TotalTime[language] = f"{hours} h {minutes} min"
            else:
                formatted_TotalTime[language] = f"{time} min"

        for i, (language, _, _, _, _) in enumerate(exerciseForProcessing):
            if language != previous_language:
                # Füge eine Sprachanweisung hinzu, wenn sich die Sprache ändert
                import_list += f"\\section{{{self.translation_to_str('language_instruction', language)}: {formatted_TotalTime[language]}}}\n"
                import_list += self.instruction_translation(language) + "\n\n\\clearpage\n\n"
                previous_language = language
            if self.exam:
                import_list += f"\\input{{../stamp/header}}\n"
            import_list += f"\\input{{{paths_exercise[i]}}}\\clearpage\n\n"

        import_list += solution

        data = data.replace("__PAPER_IMPORTS__", import_list)

        formatted_total_time = ", ".join(
            f"{language.capitalize()}: {time}" for language, time in formatted_TotalTime.items()
        )

        data = data.replace("__PAPER_TOTAL_TIME__", formatted_total_time)

        return data

    async def generating_paper(self, paper: str, information: list, paths_exercise: list,
                               exerciseForProcessing: list[tuple[str, str, str, str, int]]) -> None:

        await asyncio.to_thread(self.copy_template, paper)

        # Read the template file as a single str
        async with aiofiles.open(f"./generated/{paper}/{paper}.tex", 'r', encoding="utf-8") as f:
            data = await f.read()

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
        data = data.replace("__PAPER_MATNAM_VERSION__", self.version)

        data = self.exercise_and_times(data, exerciseForProcessing, paths_exercise)

        # Extract all unique IDs from the exerciseForProcessing list
        used_ids = {os.path.basename(path).split('_')[1] for path in paths_exercise}

        # Join the IDs into a single str separated by commas
        import_list_id = ', '.join(sorted(used_ids))

        # Replace the placeholder with the generated list of IDs
        data = data.replace("__PAPER_USED_ID__", import_list_id)

        # Write the modified content back to the file
        async with aiofiles.open(f"./generated/{paper}/{paper}.tex", 'w', encoding="utf-8") as f:
            await f.write(data)

        log.write(f"Generated paper file: ./generated/{paper}/{paper}.tex")

        return None

    async def generating_solution_paper(self, paper: str, information: list, paths_exercise: list,
                                        paths_solution: list,
                                        exerciseForProcessing: list[tuple[str, str, str, str, int]]) -> None:

        path = "solution" + paper
        await asyncio.to_thread(self.copy_template, path)

        # Read the template file as a single str
        async with aiofiles.open(f"./generated/{path}/{path}.tex", 'r', encoding="utf-8") as f:
            data = await f.read()

        # Processing __PARAMETERS__ in the template
        # [title, date, paper, description, version, revision, archive, doi, tags]
        data = data.replace("__PAPER_TITLE__", "Solution: " + information[0])
        data = data.replace("__PAPER_DATE__", information[1])
        data = data.replace("__PAPER_ID__", information[2])
        data = data.replace("__PAPER_DESCRIPTION__", information[3])
        data = data.replace("__PAPER_VERSION__", information[4])
        data = data.replace("__PAPER_REVISION__", information[5])
        data = data.replace("__PAPER_ARCHIVE__", information[6])
        data = data.replace("__PAPER_DOI__", information[7])
        data = data.replace("__PAPER_TAGS__", ' '.join(information[8]))
        data = data.replace("__PAPER_MATNAM_VERSION__", self.version)

        previous_language = None
        import_list = ""

        for i, (language, _, _, _, _) in enumerate(exerciseForProcessing):
            if language != previous_language:
                # Füge eine Sprachanweisung hinzu, wenn sich die Sprache ändert
                import_list += f"\\section{{{self.translation_to_str('solution', language)}}}\n"
                previous_language = language
            import_list += f"\\input{{{paths_solution[i]}}}\\clearpage\n"

        data = self.exercise_and_times(data, exerciseForProcessing, paths_exercise, import_list)

        # Extract all unique IDs from the exerciseForProcessing list
        used_ids = {os.path.basename(path).split('_')[1] for path in paths_exercise}

        # Join the IDs into a single str separated by commas
        import_list_id = ', '.join(sorted(used_ids))

        # Replace the placeholder with the generated list of IDs
        data = data.replace("__PAPER_USED_ID__", import_list_id)

        # Write the modified content back to the file
        async with aiofiles.open(f"./generated/{path}/{path}.tex", 'w', encoding="utf-8") as f:
            await f.write(data)

        log.write(f"Generated paper file: ./generated/{path}/{path}.tex")

        return None

    def clear_absolute(self):  # Not used for bucket creation
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

    def clear_non_pdf(self):
        # Check if the directory exists
        try:
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
        except Exception as e:
            log.write(f"Error while cleaning 'generated' directory: {e}")

    async def async_compile(self, paper, title, date, description, version, revision, archive, doi, tags,
                            paths_exercise, paths_solution, updated_exerciseForProcessing):
        await asyncio.gather(
            self.generating_paper(
                paper, [title, date, paper, description, version, revision, archive, doi, tags],
                paths_exercise, updated_exerciseForProcessing
            ),
            self.generating_solution_paper(
                paper, [title, date, paper, description, version, revision, archive, doi, tags],
                paths_exercise, paths_solution, updated_exerciseForProcessing
            )
        )

        await asyncio.gather(
            self.compile_files(paper),
            self.compile_files("solution" + paper)
        )

    async def get_exam_data(self, file: str) -> tuple[list[str], int]:
        try:
            async with aiofiles.open(file, 'r', encoding="utf-8") as f:
                content = await f.read()  # Dateiinhalt asynchron lesen
                data = json.loads(content)  # JSON-Daten aus dem Inhalt laden
        except FileNotFoundError:
            log.write(f"File '{file}' not found.")
            exit(1)
        except json.JSONDecodeError:
            log.write(f"Error decoding JSON from file '{file}'.")
            exit(1)

        keys = ["applicant", "reg-id", "institution", "issuing", "validator", "evaluator", "sdr-id", "protrack-id",
                "pid", "of-id", "location", "language", "signature", "hash", "information", "dates", "time"]
        information = []
        for key in keys:
            if key not in data:
                log.write(f"Key '{key}' not found in the file.")
                exit(1)
            information.append(data[key])
            log.write(key + " : " + str(data[key]))

        return information, int(data["time"])

    async def generate_stamp(self, applicant: list[str], time: int) -> None:
        # Copy stamp files
        stamp_dir = "./generated/stamp"
        os.makedirs(stamp_dir, exist_ok=True)
        for file_name in ["stamp.tex", "header.tex"]:
            source_path = os.path.join("./template", file_name)
            destination_path = os.path.join(stamp_dir, file_name)
            if os.path.exists(source_path):
                shutil.copy2(source_path, destination_path)
            else:
                log.write(f"File {file_name} not found in the template directory.")

        async with aiofiles.open("./generated/stamp/stamp.tex", 'r', encoding="utf-8") as f:
            template = await f.read()  # <-- await hinzufügen!

        # Creating instances
        code256_instance = c256.Code_256()
        code16_instance = c16.Code_16()

        template = template.replace("__OFFICIAL_APPLICANT__", applicant[0])

        template = template.replace("__CODE_APPLICANT__", code256_instance.text_to_tikz_html(text=applicant[0]))

        template = template.replace("__OFFICIAL_REGISTRATION_NUMBER__", applicant[1])
        template = template.replace("__OFFICIAL_INSTITUTION__", applicant[2])
        template = template.replace("__OFFICIAL_ISSUING__", applicant[3])
        template = template.replace("__OFFICIAL_VALIDATOR__", applicant[4])
        template = template.replace("__OFFICIAL_EVALUATOR__", applicant[5])
        template = template.replace("__OFFICIAL_SDR_ID__", applicant[6])
        template = template.replace("__OFFICIAL_COID__", applicant[7])
        template = template.replace("__OFFICIAL_PAPER_ID__", applicant[8])
        template = template.replace("__OFFICIAL_PAPER_REG_ID__", applicant[9])
        template = template.replace("__OFFICIAL_SUBMISSION_LOCATION__", applicant[10])

        template = template.replace("__CODE_LOCATION__", code256_instance.text_to_tikz_html(text=applicant[10]))

        template = template.replace("__OFFICIAL_CODE__", str(applicant[11]).upper())

        # Finding Language based on the translation file and code
        template = template.replace("__OFFICIAL_LANGUAGE__", self.translation_to_str("language", applicant[11]))
        template = template.replace("__OFFICIAL_SIGNATURE__", applicant[12])

        template = template.replace("__CODE_AUTH__", code16_instance.hash_to_tikz(applicant[12]))

        template = template.replace("__OFFICIAL_HASH__", applicant[13])

        template = template.replace("__CODE_HASH__", code16_instance.hash_to_tikz(applicant[13]))

        template = template.replace("__OFFICIAL_ADD_INFO__", applicant[14])

        # Dates
        template = template.replace("__OFFICIAL_ISSUING_DATE__", applicant[15][0])
        template = template.replace("__OFFICIAL_APPROVAL_DATE__", applicant[15][1])
        template = template.replace("__OFFICIAL_AVAILABILITY_DATE__", applicant[15][2])
        template = template.replace("__OFFICIAL_DEADLINE__", applicant[15][3])
        template = template.replace("__OFFICIAL_EXPIRY__", applicant[15][4])
        template = template.replace("__OFFICIAL_SIGNATURE_DATE__", applicant[15][5])

        # Format time (min) to hours and minutes

        template = template.replace("__OFFICIAL_TIME__",
                                    f"{time // 60} h {time % 60} min" if time >= 60 else f"{time} min")

        """
        https://devkid.vinlancer.de/submission/{sdr-id}/registration/{reg-id}}/signature/{signature}/registry/{of-id}
        """

        link = "https://devkid.vinlancer.de/submission/" + applicant[6] + "/registration/" + applicant[
            1] + "/signature/" + applicant[12] + "/registry/" + applicant[9]
        template = template.replace("__OFFICIAL_LINK__", link)

        template = template.replace("__CODE_ID__", code256_instance.text_to_tikz_html(text=link))

        # Break the link into two parts. One from https to signature/ and the other from signature to end

        link1 = "https://devkid.vinlancer.de/submission/" + applicant[6] + "/registration/" + applicant[
            1] + "/signature/"
        link2 = applicant[12] + "/registry/" + applicant[9]

        template = template.replace("__OFFICIAL_LINK_1__", link1)
        template = template.replace("__OFFICIAL_LINK_2__", link2)

        async with aiofiles.open("./generated/stamp/stamp.tex", 'w', encoding="utf-8") as f:
            await f.write(template)

        async with aiofiles.open("./generated/stamp/header.tex", 'r', encoding="utf-8") as f:
            template = await f.read()

        template = template.replace("__OFFICIAL_APPLICANT__", applicant[0])
        template = template.replace("__OFFICIAL_PAPER_REG_ID__", applicant[9])
        template = template.replace("__OFFICIAL_SDR_ID__", applicant[6])
        template = template.replace("__CODE_APPLICANT__", code256_instance.text_to_tikz_html(text=applicant[0]))
        template = template.replace("__CODE_ID__", code256_instance.text_to_tikz_html(text=link))

        async with aiofiles.open("./generated/stamp/header.tex", 'w', encoding="utf-8") as f:
            await f.write(template)

        return None

    async def main(self, file: str) -> typing.Optional[None]:
        log.create_log()

        log.write("Version: " + self.version)

        self.clear_non_pdf()
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

        # Check if exam JSON
        try:
            if data["applicant"] != "":
                log.write("This is an exam JSON file.")

                # TODO: Verification through API
                # TODO: Applying language

                self.exam = True
                if await self.get_exam_data(file) != None:
                    information, time = await self.get_exam_data(file)
                    if information is None:
                        log.write("Error reading exam data.")
                        return None
                    log.write(f"{information}")

                    self.language = information[11]

                    await self.generate_stamp(information, time)


                # Loading
                try:
                    with open("paper/" + data["pid"] + ".json", 'r', encoding="utf-8") as f:
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
        except KeyError:
            log.write("This is not an exam JSON file. Continue with normal paper generation.")
            pass

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
        self.sorted = data["sorted"] if data["sorted"] is not None else True

        exercise_for_processing: list[tuple[str, str, str, str]] = []

        # TODO: Process the exercise information faster by asyncio
        # TODO: Checking for new version format.
        # TODO: Caching
        exercise_for_processing = await self.phrase_exercise(exercise, exercise_for_processing)
        uuid_list: list[str] = []
        guid_list: list[str] = []
        for i, (language, file, version, raw) in enumerate(exercise_for_processing):
            log.write(f"Processing exercise: {file} {i + 1} / {len(exercise_for_processing)}")
            case, uuid, guid = await self.validating_exercise(file, uuid_list, guid_list)
            log.write("Registred UUID: " + uuid + " GUID: " + guid)
            if not case:
                log.write("Invalid exercise file: " + file)
                exit(1)
            uuid_list.append(uuid)
            guid_list.append(guid)

        updated_exerciseForProcessing: list[tuple[str, str, str, str, int]] = []
        paths_exercise: list[str] = []
        paths_solution: list[str] = []

        # ! Warning: DON'T REMOVE IT AGAIN
        for language, file, version, raw in exercise_for_processing:
            time, paths_exercise, paths_solution = self.generating_exercise(language, file, paper, version, raw,
                                                                            paths_exercise,
                                                                            paths_solution)
            updated_exerciseForProcessing.append((language, file, version, raw, time))

        # Remove every item not in the applied language for exam
        #if self.exam:
        #    for i, (language, file, version, raw, time) in enumerate(updated_exerciseForProcessing):
        #        if language != self.language:
        #            updated_exerciseForProcessing.pop(i)
        #            paths_exercise.pop(i)
        #            paths_solution.pop(i)

        # TODO: Remove items from paths_exercise and paths_solution if they are not valid and fix list
        # TODO: Fixing finding errors etc. in the output of xelatex
        #await asyncio.gather(
        #   *[self.checking_syntax(path) for path in paths_exercise],
        #   *[self.checking_syntax(path) for path in paths_solution]
        #)

        # TODO: Remove temporary
        # TODO: Adding formatting with latexident?

        # Warte auf die Fertigstellung der asynchronen Kompilierung
        await self.async_compile(paper, title, date, description, version, revision, archive, doi, tags, paths_exercise,
                                 paths_solution, updated_exerciseForProcessing)

        # Aufräumen nach Abschluss aller Schritte
        self.clear_non_pdf()

        return None


if __name__ == "__main__":
    start = datetime.datetime.now()

    if len(sys.argv) != 2:
        log.write("Usage: python matnam.py <json_file>")
        sys.exit(1)

    load_dotenv()

    exercise_dir: str = os.getenv("EXERCISE") or "./exercise"  # Directory for exercises
    difficulty: str = os.getenv(
        "DIFFICULTY") or "translation/difficulty.json"  # Information about difficulty and translation
    translation: str = os.getenv("TRANSLATION") or "translation/translation.json"  # Information about translation
    category: str = os.getenv("CATEGORY") or "translation/category.json"  # Information about category
    log.write("Exercise directory: " + exercise_dir + " Difficulty: " + difficulty + " Translation: " + translation)

    gen = Generation(exercise_dir, difficulty, translation, category)

    # Starte die asynchrone Hauptmethode
    asyncio.run(gen.main(sys.argv[1]))

    end = datetime.datetime.now()
    log.write("Execution time: " + str(end - start))
