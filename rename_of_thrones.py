#!/usr/bin/env python3

# Desired Filename Convention:
# <name>.SXXEXX.<Criterion?>.<3D?>.<resolution>.<encoding>.<bit depth>.<audio format>.<year>.<extension>
# Example: My.Show.S01E01.Criterion.3D.1080p.HEVC.10bit.DDP5.1.2023.mkv

import os
import re
import sys

# Function to extract metadata and construct a new filename
def generate_new_filename(old_filename):
    # Regular expressions for detecting common patterns
    patterns = {
        'season_episode': re.compile(r'[Ss](\d{1,2})[Ee](\d{1,2})'),
        'resolution': re.compile(r'(480p|720p|1080p|2160p)'),
        'year': re.compile(r'(\d{4})'),
        'criterion': re.compile(r'(Criterion)'),
        '3D': re.compile(r'(3D)'),
        'encoding': re.compile(r'(HEVC|x265|x264|H\.264)'),
        'bit_depth': re.compile(r'(\d{2}bit)'),
        'audio': re.compile(r'(DDP5\.1|AAC5\.1|DTS|TrueHD|Atmos|5\.1|7\.1)')
    }

    # Expanded unwanted text patterns based on the manifest.txt
    unwanted_patterns = (
        r'(-RARBG|\[YTS\]|\[YIFY\]|\[AnimeRG\]|\[TGx\]|\[bonkai77\]|\[Reaktor\]|'
        r'\[Golumpa\]|\[RH\]|\[Judas\]|\[CourseWikia\.com\]|\[FreeCourseWeb\.com\]|'
        r'BluRay|HDTV|WEBRip|BRRip|WEB-DL|BDRip|REMUX|xvid|h264|x264|HEVC|x265|'
        r'Downloaded from.*|Do not mirror|Subs|\.com|\.org|Dual Audio|Multi-Subs|'
        r'COMPLETE|REPACK|PROPER|UNRATED|DUBBED|EXTENDED|DC|HDRip|'
        r'AMZN|WEB-DL|FLUX|GalaxyTV|HMAX|Amazon|[^\w\d.\[\] ])'
    )

    # Clean the filename by removing unwanted text
    clean_filename = re.sub(unwanted_patterns, '', old_filename, flags=re.IGNORECASE)

    # Extract metadata from the cleaned filename using regex
    season_episode = patterns['season_episode'].search(clean_filename)
    criterion = patterns['criterion'].search(clean_filename)
    resolution = patterns['resolution'].search(clean_filename)
    year = patterns['year'].search(clean_filename)
    is_3d = patterns['3D'].search(clean_filename)
    encoding = patterns['encoding'].search(clean_filename)
    bit_depth = patterns['bit_depth'].search(clean_filename)
    audio = patterns['audio'].search(clean_filename)

    # Construct the new filename
    base_name = os.path.splitext(clean_filename)[0]
    new_filename_parts = [base_name.strip()]

    # Add metadata only if it's not already in the base name
    if season_episode and f"S{season_episode.group(1).zfill(2)}E{season_episode.group(2).zfill(2)}" not in base_name:
        new_filename_parts.append(f"S{season_episode.group(1).zfill(2)}E{season_episode.group(2).zfill(2)}")
    if criterion and "Criterion" not in base_name:
        new_filename_parts.append("Criterion")
    if is_3d and "3D" not in base_name:
        new_filename_parts.append("3D")
    if resolution and resolution.group(1) not in base_name:
        new_filename_parts.append(resolution.group(1))
    if encoding and encoding.group(1) not in base_name:
        new_filename_parts.append(encoding.group(1))
    if bit_depth and bit_depth.group(1) not in base_name:
        new_filename_parts.append(bit_depth.group(1))
    if audio and audio.group(1) not in base_name:
        new_filename_parts.append(audio.group(1))
    if year and year.group(1) not in base_name:
        new_filename_parts.append(year.group(1))

    # Join the parts with dots and add the original file extension
    new_filename = '.'.join(new_filename_parts) + os.path.splitext(old_filename)[1]

    # Remove any accidental double dots
    new_filename = re.sub(r'\.\.+', '.', new_filename)

    return new_filename

def main(directory):
    # Iterate over all files in the directory and rename them
    for root, dirs, files in os.walk(directory):
        for file in files:
            old_path = os.path.join(root, file)
            new_filename = generate_new_filename(file)
            new_path = os.path.join(root, new_filename)

            # Rename the file
            try:
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")
            except Exception as e:
                print(f"Failed to rename {old_path}: {e}")

if __name__ == "__main__":
    # Check if the directory path is provided
    if len(sys.argv) < 2:
        print("Usage: python rename_of_thrones.py <directory_path>")
        sys.exit(1)

    # Get the directory path from the command line argument
    directory_path = sys.argv[1]
    main(directory_path)
