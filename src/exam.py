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
