# New: Matnam (old Task-Generation)
A Python tool for generating PDF documents from structured JSON exercise data.

## Overview

This project automates the creation of exam or paper PDFs using JSON files that describe papers, exercises, and their metadata. It supports asynchronous processing and customizable templates.

## Features

- Generate PDFs from JSON definitions
- Support for multiple languages and exercise versions
- Asynchronous processing for efficiency
- Customizable LaTeX templates
- Logging and error handling

## Exercise

Exercise are in zip files.

##  Structure of the JSON files

### Paper Json

Describes the overall paper or exam.

```JSON
{
  "title": "Your Title",
  "date": "Today's date",
  "paper": "Paper ID",
  "version": "Version",
  "revision": "Revision",
  "archive": "Archive ID",
  "doi": "Your DOI (Optional)",
  "description": "The description of the paper in the abstract",
  "exercise": {
    "n1": { "language": ["de", "en", "fr"], "version": ["1.0", "1.0", "1.0"], "exercise": [1] }
  },
  "tags": ["tag1", "tag2", "tag3"]
}
```

###  Exercise Register JSON

Maps languages and versions to exercise file paths.

```json
{
  "de": { "1.0": ["n1/de/1.0/n1-de"] },
  "en": { "1.0": ["n1/en/1.0/n1-en"] },
  "UUID": "e89de9cb-5ccc-4512-a077-38f7b983aef4"
}
```

### Exercise JSON
Defines a single exercise.
```JSON
{
  "id": "No.1",
  "category": ["Shoemei"],
  "cid": "SH-1",
  "time": 5,
  "nam_score": 1.0,
  "author": "Original",
  "date": "19.04.2025",
  "UUID": "e89de9cb-5ccc-4512-a077-38f7b983aef4",
  "GUID": "21c0f2a4-1b8e-4d3b-9f5c-7a6d1e0f3a2b",
  "main": {
    "title": "Prove that $n^2 = \\sum^{{n}{2}}_{n = 1} = (2n - 1) = n^2$",
    "content": "solution/n1-de",
    "solution": "solution/n1-de"
  },
  "difficulty": 1,
  "tags": ["Induction", "Sums", "Odd Numbers", "Natural Numbers"]
}
```

## Usage
1. Place your JSON files according to the described structure.
2. Run the generator

### Environment Variables
- EXERCISE: Directory for exercises (default: ./exercise)
- DIFFICULTY: Path to difficulty/translation info (default: translation/difficulty.json)
- TRANSLATION: Path to translation info (default: translation/translation.json)

From Version Exr 1.1 onwards. The version must be in the exercise register file.
- Resources like img. etc.: Also resources are now in the exercise register file. The version must be in the exercise register file.
- Correction File for Submisisons: A Seperate folder called `correction`
- Point table: A Seperate json called `points.json` in the exercise folder. The file must be registred in the exercise file.

# TODOS

Structure of exercise files

exercise/id/language/version/things you have

Note: I use the themes Material Darker and at daytime Solarized Light (Material).

TODO: Creating a website with a database and download api.

TODO: Create USERS etc. Database and API, also a new type of section (Correction).
TODO: Max Points
