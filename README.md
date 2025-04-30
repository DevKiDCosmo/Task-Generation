# Task-Generation
Generating PDFs with JSON Exercise

# Structure of the JSON files

## PAPER

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
    "n1": { "language": ["de", "en", "fr"], "version": ["1.0", "1.0", "1.0"], "exercise": [1] },
    "n4": { "language": ["de", "en"], "version": ["1.0d", "1.1e"], "exercise": [1, 2, 3, 4] },
    "n5": { "language": ["de", "en"], "version": ["1.0", "1.0"], "exercise": [1] }
  },
  "tags": ["tag1", "tag2", "tag3"]
}
```

## EXERCISE REGISTER

```json
{
  "de": {
    "1.0": ["n1/de/1.0/n1-de"]
  },
  "en": {
    "1.0": ["n1/en/1.0/n1-en"]
  },
  "fr": {
    "1.0": ["n1/fr/1.0/n1-fr"]
  },
  "UUID": "e89de9cb-5ccc-4512-a077-38f7b983aef4"
}

```

## EXERCISE

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
    "title": "Beweise, dass $n^2 = \\sum^{{n}{2}}_{n = 1} = (2n - 1) = n^2$",
    "content": "solution/n1-de",
    "solution": "solution/n1-de"
  },
  "difficulty": 1,
  "tags": ["Induktion", "Summen", "Ungerade Zahlen", "Naturelle Zahlen"]
}
```

Structure of exercise files

exercise/id/language/version/things you have

Note: I use the themes Material Darker and at daytime Solarized Light (Material).


TODO: Create USERS etc. Database and API, also a new type of section (Correction).
TODO: Max Points