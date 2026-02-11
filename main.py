# FLICKRARCHIVES
# Rebuild original Flickr photo library structure from the ZIP downloads FLICKR provides
# NOTE - FLICK download ZIP format is of November 2025 (please check as FLICKR changes the format)
# This is a Python rewrite from https://github.com/sebastian-raubach/frickl

# main.py  (clean version – debug prints removed)
import zipfile
import json
import shutil
from pathlib import Path
from tqdm import tqdm
import re
import os
from dotenv import load_dotenv


def rebuild_flickr_library(input_folder: str, output_folder: str, dry_run: bool = False):
    input_path = Path(input_folder).resolve()
    output_path = Path(output_folder).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    temp_extract = output_path / "__temp_extraction__"
    if temp_extract.exists():
        shutil.rmtree(temp_extract)
    temp_extract.mkdir(exist_ok=True)

    # Step 1: Read albums.json
    print("Step 1 – Reading albums.json from part1 ZIP...")
    album_paths = {}
    photo_to_albums = {}

    part1_name = "72157724414707620_3d57a31755f7_part1.zip"
    part1_zip = input_path / part1_name

    if not part1_zip.is_file():
        print(f"ERROR: Could not find {part1_name}")
        return

    with zipfile.ZipFile(part1_zip) as zf:
        if "albums.json" not in zf.namelist():
            print("ERROR: albums.json not found")
            return

        with zf.open("albums.json") as f:
            data = json.load(f)

        for album in data.get("albums", []):
            album_id = str(album.get("id"))
            title = album.get("title", "Untitled Album").strip()
            safe_title = re.sub(r'[<>:"/\\|?*]', "_", title) or "Untitled"
            folder = output_path / safe_title
            folder.mkdir(exist_ok=True)
            album_paths[album_id] = folder

            for photo_id in album.get("photos", []):
                photo_str = str(photo_id)
                photo_to_albums.setdefault(photo_str, []).append(album_id)

    print(f"Found {len(album_paths)} albums • Mapped {len(photo_to_albums)} unique photos")

    # Step 2: Extract all media
    print("\nStep 2 – Extracting media files...")
    extracted_count = 0

    for zip_path in tqdm(list(input_path.glob("*.zip")), desc="Extracting"):
        with zipfile.ZipFile(zip_path) as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                fname_lower = Path(info.filename).name.lower()
                if fname_lower.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.heic')):
                    zf.extract(info, temp_extract)
                    extracted_count += 1

    print(f"Extracted {extracted_count} files")

    # Step 3: Organise
    print("\nStep 3 – Placing files into albums...")
    uncategorised = output_path / "00 - Uncategorised (not in any album)"
    uncategorised.mkdir(exist_ok=True)

    moved = 0
    multi_copies = 0
    unmatched = 0

    for media_file in tqdm(list(temp_extract.rglob("*")), desc="Organising"):
        if not media_file.is_file():
            continue

        stem = media_file.stem
        parts = stem.split('_')
        photo_id = None

        if len(parts) >= 3:
            candidate = parts[-2]
            if candidate.isdigit() and len(candidate) >= 9:
                photo_id = candidate

        if photo_id is None:
            match = re.search(r'(\d{9,})', stem)
            if match:
                photo_id = match.group(1)

        if photo_id is None:
            if not dry_run:
                shutil.move(str(media_file), uncategorised / media_file.name)
            unmatched += 1
            continue

        album_ids = photo_to_albums.get(photo_id, [])

        if not album_ids:
            if not dry_run:
                shutil.move(str(media_file), uncategorised / media_file.name)
            unmatched += 1
            continue

        # Move to primary album
        target_folder = album_paths.get(album_ids[0], uncategorised)
        target = target_folder / media_file.name

        if target.exists():
            target = target_folder / f"{media_file.stem}_dup{media_file.suffix}"

        if not dry_run:
            shutil.move(str(media_file), target)
        moved += 1

        # Copies for other albums
        for aid in album_ids[1:]:
            copy_folder = album_paths.get(aid, uncategorised)
            copy_target = copy_folder / media_file.name
            if not dry_run:
                shutil.copy2(target, copy_target)
            multi_copies += 1

    if not dry_run:
        shutil.rmtree(temp_extract)

    print("\nFinished!")
    print(f"   Albums created            : {len(album_paths)}")
    print(f"   Files placed in albums    : {moved}")
    print(f"   Extra copies made         : {multi_copies}")
    print(f"   Files in Uncategorised    : {unmatched}")


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Read configuration from environment variables
    input_folder = os.getenv("INPUT_FOLDER")
    output_folder = os.getenv("OUTPUT_FOLDER", "Flickr Rebuilt")
    dry_run = os.getenv("DRY_RUN", "false").lower() in ("true", "1", "yes")

    # Validate required parameters
    if not input_folder:
        print("ERROR: INPUT_FOLDER must be specified in .env file")
        exit(1)

    rebuild_flickr_library(input_folder, output_folder, dry_run)
