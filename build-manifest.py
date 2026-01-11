#!/usr/bin/env python3
"""
Comic Manifest Builder for Dan Comics Website

This script scans the Website folder and generates a manifest.json file
containing all comics organized by series and subfolders.

Usage:
    python3 build-manifest.py

Run this script whenever you add new comics to automatically update the manifest.
"""

import os
import json
from pathlib import Path
from datetime import datetime

# Configuration
WEBSITE_DIR = "Website"
OUTPUT_FILE = "manifest.json"
IMAGE_EXTENSIONS = {".jpeg", ".jpg", ".png", ".gif", ".heic", ".pdf"}
EXCLUDED_FILES = {"Background.JPG", ".DS_Store"}

def is_comic_file(filename):
    """Check if a file is a comic (image or PDF)."""
    path = Path(filename)
    return (
        path.suffix.lower() in IMAGE_EXTENSIONS
        and path.name not in EXCLUDED_FILES
    )

def scan_folder(folder_path):
    """Scan a folder and return list of comic files."""
    comics = []

    if not os.path.exists(folder_path):
        return comics

    try:
        for item in sorted(os.listdir(folder_path)):
            if item.startswith('.'):
                continue

            item_path = os.path.join(folder_path, item)

            # Only process files, not subdirectories
            if os.path.isfile(item_path) and is_comic_file(item):
                # Get file info
                file_stat = os.stat(item_path)
                file_ext = Path(item).suffix.lower()

                comics.append({
                    "name": item,
                    "path": item_path.replace("\\", "/"),  # Use forward slashes
                    "isPdf": file_ext == ".pdf",
                    "size": file_stat.st_size,
                    "modified": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                })
    except Exception as e:
        print(f"Warning: Error scanning {folder_path}: {e}")

    return comics

def scan_series(series_path, series_name):
    """Scan a series folder for comics and subfolders."""
    series_data = {
        "name": series_name,
        "folder": series_name,
        "subFolders": [],
        "comics": []
    }

    if not os.path.exists(series_path):
        return series_data

    # First, scan for subfolders
    try:
        items = sorted(os.listdir(series_path))
        for item in items:
            if item.startswith('.'):
                continue

            item_path = os.path.join(series_path, item)

            if os.path.isdir(item_path):
                # It's a subfolder
                subfolder_comics = scan_folder(item_path)
                if subfolder_comics:  # Only include if it has comics
                    series_data["subFolders"].append({
                        "name": item,
                        "path": f"{series_name}/{item}",
                        "comics": subfolder_comics
                    })

        # If there are no subfolders, scan the main folder for comics
        if not series_data["subFolders"]:
            series_data["comics"] = scan_folder(series_path)

    except Exception as e:
        print(f"Warning: Error scanning series {series_name}: {e}")

    return series_data

def build_manifest():
    """Build the complete manifest of all comics."""
    print("🎨 Building Comic Manifest...")
    print(f"📁 Scanning directory: {WEBSITE_DIR}")

    manifest = {
        "generated": datetime.now().isoformat(),
        "version": "1.0",
        "series": []
    }

    if not os.path.exists(WEBSITE_DIR):
        print(f"❌ Error: {WEBSITE_DIR} directory not found!")
        return None

    # Scan all series folders
    try:
        series_folders = sorted([
            item for item in os.listdir(WEBSITE_DIR)
            if os.path.isdir(os.path.join(WEBSITE_DIR, item))
            and not item.startswith('.')
        ])

        for series_name in series_folders:
            series_path = os.path.join(WEBSITE_DIR, series_name)
            series_data = scan_series(series_path, series_name)

            # Count total comics
            total_comics = len(series_data["comics"])
            for subfolder in series_data["subFolders"]:
                total_comics += len(subfolder["comics"])

            print(f"  ✓ {series_name}: {total_comics} comics")

            manifest["series"].append(series_data)

    except Exception as e:
        print(f"❌ Error building manifest: {e}")
        return None

    return manifest

def save_manifest(manifest):
    """Save the manifest to a JSON file."""
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Manifest saved to {OUTPUT_FILE}")

        # Print summary
        total_series = len(manifest["series"])
        total_comics = sum(
            len(s["comics"]) + sum(len(sf["comics"]) for sf in s["subFolders"])
            for s in manifest["series"]
        )
        print(f"📊 Summary: {total_series} series, {total_comics} total comics")

        return True
    except Exception as e:
        print(f"❌ Error saving manifest: {e}")
        return False

def main():
    """Main function."""
    print("=" * 60)
    print("  Dan Comics - Manifest Builder")
    print("=" * 60)
    print()

    manifest = build_manifest()

    if manifest:
        if save_manifest(manifest):
            print("\n✨ Done! Commit and push manifest.json to update the website.")
            print("\nNext steps:")
            print("  1. git add manifest.json")
            print("  2. git commit -m 'Update comics manifest'")
            print("  3. git push")
            return 0

    print("\n❌ Failed to build manifest")
    return 1

if __name__ == "__main__":
    exit(main())
