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
        '3D': re.compile(r'(3D)'),
        'encoding': re.compile(r'(HEVC|x265|x264|H\.264)'),
        'bit_depth': re.compile(r'(\d{2}bit)'),
        'audio': re.compile(r'(DDP5\.1|AAC5\.1|DTS|TrueHD|Atmos|5\.1|7\.1)')
    }

    # Extract metadata from the filename using regex
    season_episode = patterns['season_episode'].search(old_filename)
    resolution = patterns['resolution'].search(old_filename)
    year = patterns['year'].search(old_filename)
    is_3d = patterns['3D'].search(old_filename)
    encoding = patterns['encoding'].search(old_filename)
    bit_depth = patterns['bit_depth'].search(old_filename)
    audio = patterns['audio'].search(old_filename)

    # Construct the new filename
    base_name = os.path.splitext(old_filename)[0]
    new_filename = base_name

    if season_episode:
        new_filename += f".S{season_episode.group(1).zfill(2)}E{season_episode.group(2).zfill(2)}"
    if is_3d:
        new_filename += ".3D"
    if resolution:
        new_filename += f".{resolution.group(1)}"
    if encoding:
        new_filename += f".{encoding.group(1)}"
    if bit_depth:
        new_filename += f".{bit_depth.group(1)}"
    if audio:
        new_filename += f".{audio.group(1)}"
    if year:
        new_filename += f".{year.group(1)}"

    # Append the original extension back to the new filename
    new_filename += os.path.splitext(old_filename)[1]

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

