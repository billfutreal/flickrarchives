# Flickr Album Rebuilder (Python)

**Offline Flickr export organizer** – Rebuilds your Flickr photo & video library into proper album folders using only the downloaded ZIP files.  
No API key required. Works with Flickr's standard data export format.

This script was created to process a specific Flickr export structure where:
- Album metadata lives in `albums.json` inside one metadata ZIP file
- Actual photos/videos are spread across multiple ZIP parts
- Filenames contain the Flickr photo ID in a non-standard position

## Features

- 100% offline – no Flickr API or internet connection needed
- Reads album structure from `albums.json`
- Matches photos/videos by extracting the numeric photo ID from filenames
- Creates one folder per album with original filenames preserved
- Handles photos that appear in multiple albums (makes copies)
- Collects unmatched files (orphans, screenshots, non-album items) in a clearly named folder
- Supports photos (jpg, jpeg, png, gif, heic) and videos (mp4, mov)
- Progress bars via `tqdm`
- Dry-run mode to preview what will happen
- Configuration via `.env` file for easy setup

## Current results (example run)

- Albums found: **87**
- Unique photos mapped in albums: **2959**
- Total media files extracted: **8563**
- Files placed in albums: **~2953**
- Files sent to Uncategorised: **~5610** (mostly non-albumed items, avatars, screenshots, etc.)

## Requirements

- Python 3.8+
- Two external packages:

```bash
pip install tqdm python-dotenv
```

## Installation

1. Clone or download this repository
2. (Recommended) Create & activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate          # Windows
```
or
```bash
source venv/bin/activate       # macOS / Linux
```

3. Install the dependencies:

```bash
pip install tqdm python-dotenv
```

## Configuration

1. Edit the `.env` file in the same directory as `main.py`
2. Set the required `INPUT_FOLDER` path to your Flickr ZIP files location
3. Optionally adjust `OUTPUT_FOLDER` and `DRY_RUN` settings

Example `.env` file:

```bash
# INPUT_FOLDER - Required: Folder containing Flickr ZIP files
INPUT_FOLDER=C:\Users\YourName\Pictures\FLICKR

# OUTPUT_FOLDER - Optional: Where to create the rebuilt album structure
# Default: "Flickr Rebuilt"
OUTPUT_FOLDER=D:\Photos\Flickr Rebuilt Library

# DRY_RUN - Optional: Set to true to simulate without making changes
# Valid values: true, false, 1, 0, yes, no
# Default: false
DRY_RUN=false
```

## Usage

1. Place all your Flickr export ZIP files into one folder
2. Configure the `.env` file with your paths
3. Run the script:

**Dry run (strongly recommended first):**
```bash
# Set DRY_RUN=true in .env file, then:
python main.py
```

**Real run:**
```bash
# Set DRY_RUN=false in .env file, then:
python main.py
```

## Configuration Options

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `INPUT_FOLDER` | Folder containing all `*.zip` files | - | Yes |
| `OUTPUT_FOLDER` | Destination folder for album folders | `Flickr Rebuilt` | No |
| `DRY_RUN` | Simulate only – no files are moved or copied | `false` | No |

## Project files

```
├── main.py               # The complete script
├── .env                  # Configuration file
├── README.md             # This file
└── requirements.txt      # Dependencies: tqdm, python-dotenv
```

## How it works (high level)

1. Reads `albums.json` from the metadata ZIP (`72157724414707620_3d57a31755f7_part1.zip`)
2. Builds a mapping: photo ID → list of album IDs
3. Extracts all photos/videos from all ZIP files into a temporary folder
4. For each file:
   - Extracts the Flickr photo ID from the filename (usually the long number before `_o.jpg` / `_m.jpg` etc.)
   - Moves the file to the first album it belongs to
   - Copies it to any additional albums
   - Places unmatched files in `00 - Uncategorised (not in any album)`

## Limitations

- No titles, descriptions, or tags are embedded (your export format does not include per-photo metadata JSON files)
- Some files will always end up in Uncategorised (normal for Flickr exports – includes profile pictures, deleted items, non-albumed photos, etc.)
- Folder names are sanitized (invalid characters replaced with `_`)

## License

MIT License – feel free to use, modify, and share.

## Acknowledgments

- Inspired by original tools like Frickl
- Uses `tqdm` for clean progress bars

Made in 2025–2026  
Happy Flickr-liberating!
