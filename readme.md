# Flickr Album Rebuilder (Python)

**Offline Flickr export organizer** — Rebuilds your Flickr photo & video library into proper album folders using only the downloaded ZIP files.  
No API key required. Works with Flickr's standard data export format.

This script was created to process a specific Flickr export structure where:
- Album metadata lives in `albums.json` inside one metadata ZIP file
- Actual photos/videos are spread across multiple ZIP parts
- Filenames contain the Flickr photo ID in a non-standard position

## Features

- 100% offline — no Flickr API or internet connection needed
- Reads album structure from `albums.json`
- Matches photos/videos by extracting the numeric photo ID from filenames
- Creates one folder per album with original filenames preserved
- Handles photos that appear in multiple albums (makes copies)
- Collects unmatched files (orphans, screenshots, non-album items) in a clearly named folder
- Supports photos (jpg, jpeg, png, gif, heic) and videos (mp4, mov)
- Progress bars via `tqdm`
- Dry-run mode to preview what will happen

## Current results (example run)

- Albums found: **87**
- Unique photos mapped in albums: **2959**
- Total media files extracted: **8563**
- Files placed in albums: **~2953**
- Files sent to Uncategorised: **~5610** (mostly non-albumed items, avatars, screenshots, etc.)

## Requirements

- Python 3.8+
- Only one external package:

bash
pip install tqdm
Installation

Clone or download this repository
(Recommended) Create & activate a virtual environment:

Bashpython -m venv venv
venv\Scripts\activate          # Windows
or
source venv/bin/activate       # macOS / Linux

Install the dependency:

Bashpip install tqdm
Usage
Place all your Flickr export ZIP files into one folder.
Dry run (strongly recommended first)
Bashpython main.py "C:\Users\YourName\Pictures\FLICKR" -o "C:\Users\YourName\Pictures\FLICKROUTPUT" --dry-run
Real run
Bashpython main.py "C:\Users\YourName\Pictures\FLICKR" -o "D:\Photos\Flickr Rebuilt Library"
Command-line options

Argument Description DefaultinputFolder containing all *.zip files(required)-o, --outputDestination folder for album foldersFlickr Rebuilt--dry-runSimulate only — no files are moved or copiedoff
Project files
text.
├── main.py               # The complete script
├── README.md             # This file
└── requirements.txt      # Just one line: tqdm
## How it works (high level)
Reads albums.json from the metadata ZIP (72157724414707620_3d57a31755f7_part1.zip)
Builds a mapping: photo ID → list of album IDs
Extracts all photos/videos from all ZIP files into a temporary folder
For each file:
Extracts the Flickr photo ID from the filename (usually the long number before _o.jpg / _m.jpg etc.)
Moves the file to the first album it belongs to
Copies it to any additional albums
Places unmatched files in 00 - Uncategorised (not in any album)

## Limitations

No titles, descriptions, or tags are embedded (your export format does not include per-photo metadata JSON files)
Some files will always end up in Uncategorised (normal for Flickr exports — includes profile pictures, deleted items, non-albumed photos, etc.)
Folder names are sanitized (invalid characters replaced with _)

## License
MIT License — feel free to use, modify, and share.
Acknowledgments

Inspired by original tools like Frickl
Uses tqdm for clean progress bars

Made in 2025–2026
Happy Flickr-liberating!