#!/usr/bin/env python3

# Desired Filename Convention:
# <name>.SXXEXX.<Criterion?>.<3D?>.<resolution>.<encoding>.<bit depth>.<audio format>.<year>.<extension>
# Example: My.Show.S01E01.Criterion.3D.1080p.HEVC.10bit.DDP5.1.2023.mkv

import os
import re
import sys

# Function to extract metadata and construct a new filename
def generate_new_name(old_name, is_directory=False):
    # Regular expressions for detecting common patterns
    patterns = {
        'season_episode': re.compile(r'[Ss](\d{1,2})[Ee](\d{1,2})'),
        'season_range': re.compile(r'[Ss](\d{1,2})-[Ss](\d{1,2})'),
        'resolution': re.compile(r'(480p|720p|1080p|2160p)'),
        'year': re.compile(r'(\d{4})'),
        'criterion': re.compile(r'(Criterion)'),
        '3D': re.compile(r'(3D)'),
        'encoding': re.compile(r'(HEVC|x265|x264|H\.264)'),
        'bit_depth': re.compile(r'(\d{2}bit)'),
        'audio': re.compile(r'(DDP5\.1|AAC5\.1|DTS|TrueHD|Atmos|5\.1|7\.1)')
    }

    # Expanded unwanted text patterns including new patterns from the manifest
    unwanted_patterns = (
        r'\b(RARBG|YTS|YIFY|AnimeRG|TGx|bonkai77|Reaktor|Golumpa|RH|Judas|CourseWikia\.com|'
        r'FreeCourseWeb\.com|BluRay|HDTV|WEBRip|BRRip|WEB-DL|BDRip|REMUX|xvid|h264|'
        r'Downloaded from.*|Do not mirror|Subs|\.com|\.org|Dual Audio|Multi-Subs|'
        r'COMPLETE|PROPER|UNRATED|DUBBED|EXTENDED|DC|HDRip|AMZN|FLUX|'
        r'GalaxyTV|HMAX|Amazon|SARTRE|REPACK|NFO|EVO|Sample|HiQVE|FLAC|XviD|PublicHD|'
        r'H\.265|H\.264|DDP5\.1|DD5\.1|DD2\.0|DUAL-AUDIO|NF|publichd|GalaxyRG|'
        r'SARTRE|AnimeRG|YTS.LT|YTS.AM|YTS.MX|bonkai77|Reaktor|Judas|RH|Golumpa|'
        r'TGx|ANiHLS|DB|GalaxyTV|PublicHD|COLLECTiVE|FLUX|NOGRP|YIFY|EVO|HODL|'
        r'Ghost|BONE|Vyndros|EMBER|SSK|LAZYCUNTS|SuccessfullCrab|PxL|'
        r'WEBRip|BluRay|WEB-DL|BDRip|HDTV|HDRip|DVDrip|REMUX|xvid|x264|'
        r'HEVC|x265|AAC|10bit|8bit|AAC5.1|DTS|FLAC|DD5.1|DDP5.1|5.1|7.1|Atmos|'
        r'Dual-Audio|Multi-Subs|COMPLETE|REPACK|UNRATED|DUBBED|EXTENDED|DC|HSBS|'
        r'SUBBED|RAW|HDR|WEBRip|DSNP|AMZN|ATVP|HMAX|HMAX.WEBRip|HMAX.WEB-DL|'
        r'HMAX.WEB|Downloaded from.*|Torrent downloaded from.*|Sample.*|Do not mirror|'
        r'Readme.*|Subs|EXTRAS|Featurettes|DO_NOT_MIRROR|RARBG|Demonoid|1337x|'
        r'ETTV|ProstyleX|Angietorrents|Glodls|Thepiratebay|Katcr|CourseWikia|'
        r'FreeCourseWeb|TutsGalaxy)\b'
    )

    # Handle extensions like '.mkv.part'
    partial_extensions = ['.part', '.crdownload', '.!ut']  # Common temporary/partial extensions

    # Separate base name and extension(s)
    if not is_directory:
        # Split the filename to handle multi-part extensions
        base_name, extension = os.path.splitext(old_name)
        while any(base_name.endswith(ext) for ext in partial_extensions):
            # If the base name ends with a partial extension, append it to the current extension
            base_name, extra_extension = os.path.splitext(base_name)
            extension = extra_extension + extension
        full_extension = extension  # The full extension chain, such as '.mkv.part'
    else:
        base_name, full_extension = old_name, ""

    # Determine if the name is a single word (considering periods as separators)
    if len(re.split(r'[.\s]+', base_name)) == 1:
        return old_name

    # Preserve content inside brackets (e.g., [TGx]) unless it's in the unwanted patterns
    base_name = re.sub(r'\[(' + unwanted_patterns + r')\]', '', base_name, flags=re.IGNORECASE)

    # Clean the name by removing unwanted text, but keep encoding information
    clean_name = re.sub(unwanted_patterns, '', base_name, flags=re.IGNORECASE)

    # Remove redundant periods introduced by removing unwanted patterns
    clean_name = re.sub(r'\.\.+', '.', clean_name).strip('.')

    # Remove any trailing hyphens, dots, or spaces left after cleaning
    clean_name = re.sub(r'[-.\s]+$', '', clean_name)

    # Extract metadata from the cleaned name using regex
    season_episode = patterns['season_episode'].search(clean_name)
    season_range = patterns['season_range'].search(clean_name)
    criterion = patterns['criterion'].search(clean_name)
    resolution = patterns['resolution'].search(clean_name)
    year = patterns['year'].search(clean_name)
    is_3d = patterns['3D'].search(clean_name)
    encoding = patterns['encoding'].search(clean_name)
    bit_depth = patterns['bit_depth'].search(clean_name)
    audio = patterns['audio'].search(clean_name)

    # Construct the new name
    new_name_parts = [clean_name.strip()]

    # Add metadata only if it's not already in the base name
    if season_episode and f"S{season_episode.group(1).zfill(2)}E{season_episode.group(2).zfill(2)}" not in clean_name:
        new_name_parts.append(f"S{season_episode.group(1).zfill(2)}E{season_episode.group(2).zfill(2)}")
    elif season_range and f"S{season_range.group(1).zfill(2)}-S{season_range.group(2).zfill(2)}" not in clean_name:
        new_name_parts.append(f"S{season_range.group(1).zfill(2)}-S{season_range.group(2).zfill(2)}")
    if criterion and "Criterion" not in clean_name:
        new_name_parts.append("Criterion")
    if is_3d and "3D" not in clean_name:
        new_name_parts.append("3D")
    if resolution and resolution.group(1) not in clean_name:
        new_name_parts.append(resolution.group(1))
    if encoding and encoding.group(1) not in clean_name:
        new_name_parts.append(encoding.group(1))
    if bit_depth and bit_depth.group(1) not in clean_name:
        new_name_parts.append(bit_depth.group(1))
    if audio and audio.group(1) not in clean_name:
        new_name_parts.append(audio.group(1))
    if year and year.group(1) not in clean_name:
        new_name_parts.append(year.group(1))

    # Join the parts with dots
    new_name = '.'.join(new_name_parts)

    # Remove any accidental double dots or trailing unwanted characters
    new_name = re.sub(r'\.\.+', '.', new_name)
    new_name = re.sub(r'[-.\s]+(?=\.)', '', new_name)  # Remove any trailing hyphens or spaces before the extension

    # Add back the file extension if it's a file
    if not is_directory:
        new_name += full_extension

    return new_name

def main(directory):
    # Iterate over files and directories in the directory and its subdirectories up to a depth of 2
    for root, dirs, files in os.walk(directory):
        # Calculate the depth relative to the starting directory
        depth = root[len(directory):].count(os.sep)
        if depth <= 2:  # Correct depth limit to 2
            # Rename files
            for file in files:
                old_path = os.path.join(root, file)
                new_filename = generate_new_name(file)
                new_path = os.path.join(root, new_filename)

                # Rename the file
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {old_path} -> {new_path}")
                except Exception as e:
                    print(f"Failed to rename {old_path}: {e}")

            # Rename directories, only if empty or after contents have been renamed
            for dir in dirs:
                old_dir_path = os.path.join(root, dir)

                # First, recursively rename the contents if any
                main(old_dir_path)  # Recursively process the subdirectory

                new_dir_name = generate_new_name(dir, is_directory=True)
                new_dir_path = os.path.join(root, new_dir_name)

                # Check if new directory name already exists
                if os.path.exists(new_dir_path):
                    print(f"Skipping rename: {new_dir_path} already exists.")
                    continue

                # Rename the directory if the new name is different and does not conflict
                if new_dir_name != dir:
                    try:
                        os.rename(old_dir_path, new_dir_path)
                        print(f"Renamed directory: {old_dir_path} -> {new_dir_path}")
                    except Exception as e:
                        print(f"Failed to rename directory {old_dir_path}: {e}")

if __name__ == "__main__":
    # Check if the directory path is provided
    if len(sys.argv) < 2:
        print("Usage: python rename_of_thrones.py <directory_path>")
        sys.exit(1)

    # Get the directory path from the command line argument
    directory_path = sys.argv[1]
    main(directory_path)
