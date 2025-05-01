import asyncio
import datetime
import json
import os
import sys

import aiofiles
from dotenv import load_dotenv

import genadv
from util import log as lg
from code_gen import code_16 as c16
from code_gen import code_256 as c256

log = lg.Log()


class gen_exam():
    def __init__(self, exerciseDIR: str, difficulty_: str, translation_: str):
        self.exercise_dir = exerciseDIR
        self.difficulty = difficulty_
        self.translation = translation_

    async def translation_to_str(self, translation_key: str, language: str) -> str:
        try:
            async with aiofiles.open(self.translation, 'r', encoding="utf-8") as f:
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

    async def generate_stamp(self, applicant: list[str]):
        async with aiofiles.open("./template/stamp.tex", 'r', encoding="utf-8") as f:
            template = await f.read()  # <-- await hinzufügen!

        template = template.replace("__OFFICIAL_APPLICANT__", applicant[0])

        code256_instance = c256.Code_256()
        code_author = code256_instance.text_to_tikz_html(code256_instance, text=applicant[0])

        template = template.replace("__OFFICIAL_REGISTRATION_NUMBER__", applicant[1])
        template = template.replace("__OFFICIAL_INSTITUTION__", applicant[2])
        template = template.replace("__OFFICIAL_ISSUING__", applicant[3])
        template = template.replace("__OFFICIAL_VALIDATOR__", applicant[4])
        template = template.replace("__OFFICIAL_EVALUATOR__", applicant[5])
        template = template.replace("__OFFICIAL_SDR_ID__", applicant[6])
        template = template.replace("__OFFICIAL_COID__", applicant[7])
        template = template.replace("__OFFICIAL_PAPER_ID__", applicant[8])
        template = template.replace("__OFFICIAL_PAPER_REG_ID__", applicant[9])
        template = template.replace("__OFFICIAL__SUBMISSION_LOCATION__", applicant[10])

        code_location = c256.Code_256.text_to_tikz_html(text=applicant[10])

        template = template.replace("__OFFICIAL_CODE__", str(applicant[11]).upper())

        # Finding Language based on the translation file and code
        template = template.replace("__OFFICIAL_LANGUAGE__", await self.translation_to_str("language", applicant[11]))
        template = template.replace("__OFFICIAL_SIGNATURE__", applicant[12])

        signature = c16.Code_16.text_to_tikz_html(text=applicant[12])

        template = template.replace("__OFFICIAL_HASH__", applicant[13])

        hash = c16.Code_16.text_to_tikz_html(text=applicant[13])

        template = template.replace("__OFFICIAL_ADD_INFO__", applicant[14])

        """
        https://devkid.vinlancer.de/submission/{sdr-id}/registration/{reg-id}}/signature/{signature}/registry/{of-id}
        """

        link = "https://devkid.vinlancer.de/submission/" + applicant[6] + "/registration/" + applicant[
            1] + "/signature/" + applicant[12] + "/registry/" + applicant[9]
        template = template.replace("__OFFICIAL_LINK__", link)

        link = c256.Code_256.text_to_tikz_html(text=link)

        # Break the link into two parts. One from https to signature/ and the other from signature to end

        link1 = "https://devkid.vinlancer.de/submission/" + applicant[6] + "/registration/" + applicant[
            1] + "/signature/"
        link2 = applicant[12] + "/registry/" + applicant[9]

        template = template.replace("__OFFICIAL_LINK_1__", link1)
        template = template.replace("__OFFICIAL_LINK_2__", link2)

        async with aiofiles.open("../generated/stamp/" + applicant[1] + ".tex", 'w', encoding="utf-8") as f:
            f.write(template)

        # Generate a tex file for every code of c256 and c16
        async with aiofiles.open("../generated/stamp/" + applicant[1] + "_code_256.tex", 'w', encoding="utf-8") as f:
            f.write(code_author)
        async with aiofiles.open("../generated/stamp/" + applicant[1] + "_code_location.tex", 'w', encoding="utf-8") as f:
            f.write(code_location)
        async with aiofiles.open("../generated/stamp/" + applicant[1] + "_code_signature.tex", 'w', encoding="utf-8") as f:
            f.write(signature)
        async with aiofiles.open("../generated/stamp/" + applicant[1] + "_code_hash.tex", 'w', encoding="utf-8") as f:
            f.write(hash)
        async with aiofiles.open("../generated/stamp/" + applicant[1] + "_link.tex", 'w', encoding="utf-8") as f:
            f.write(link)



    async def main(self, exam: str):
        # Generate folders

        if not os.path.exists("./generated/stamp"):
            os.makedirs("./generated/stamp")

        exam_data = await self.get_exam_data(exam)
        if exam_data is None:
            log.write("Error: No exam data found.")
            return
        await self.generate_stamp(exam_data)

        log.write(f"Exam data: {exam_data}")


if __name__ == "__main__":

    # Starting Timer
    start = datetime.datetime.now()

    if len(sys.argv) != 2:
        log.write("Usage: python generation.py <exam>")
        sys.exit(1)

    load_dotenv()

    exercise_dir: str = os.getenv("EXERCISE") or "./exercise"  # Directory for exercises
    difficulty: str = os.getenv(
        "DIFFICULTY") or "translation/difficulty.json"  # Information about difficulty and translation
    translation: str = os.getenv("TRANSLATION") or "translation/translation.json"  # Information about translation

    log.write("Exercise directory: " + exercise_dir + " Difficulty: " + difficulty + " Translation: " + translation)

    gen = gen_exam(exercise_dir, difficulty, translation)

    # Starte die asynchrone Hauptmethode
    asyncio.run(gen.main(sys.argv[1]))

    end = datetime.datetime.now()
    log.write("Execution time: " + str(end - start))
