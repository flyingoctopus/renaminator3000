# Rename of Thrones 🏰

Welcome to **Rename of Thrones** — the ultimate tool for bringing order to the chaotic filenames in your directory! Now with support for the Criterion Collection, 3D movies, and all the nerdy metadata you could ever need. 📁✨

## What Does It Do?

The **Rename of Thrones** script scans through the files in a specified directory (and its immediate subdirectories) and renames them according to the following format:

```shell
<name>.SXXEXX.<Criterion?>.<3D?>.<resolution>.<encoding>.<bit depth>.<audio format>.<year>.<extension>
```

### Example:
```shell
The.Great.Show.S01E01.Criterion.3D.1080p.HEVC.10bit.DDP5.1.2023.mkv
```


## Features

- **Recursion Depth of 2**: Processes files in the specified directory and its immediate subdirectories. No deeper!
- **Metadata Extraction**: Automatically identifies and retains essential metadata like seasons, episodes, resolution, encoding, bit depth, audio format, year, 3D format, and even whether it's part of the Criterion Collection!
- **Superfluous Text Removal**: Say goodbye to ugly filenames with junk like `-RARBG`, `WEBRip`, `x264`, and more.
- **Python-Powered**: Uses Python to smartly parse and rename files. 🐍

## Usage

1. **Save the Script**: Download or save `rename_of_thrones.py` to your local machine.
2. **Open Terminal or Command Prompt**: Navigate to the directory where you saved `rename_of_thrones.py`.
3. **Run the Script with the Directory Path**:

    ```bash
    python rename_of_thrones.py /path/to/client_directory
    ```

   Replace `/path/to/client_directory` with the actual path of the directory containing the files you want to rename.

## Requirements

- Python 3.x 🐍 (Because old Python is so last decade!)
- Basic knowledge of using the command line (or at least how to copy-paste commands)

## Notes

- **Backup Your Files**: Before running the script, make sure you have backups. Rename of Thrones takes no prisoners and shows no mercy! 🏴‍☠️
- **Customization**: Feel free to tweak the script to add more rules or metadata checks as needed.
- **Testing**: Start with a small set of files to make sure it works as expected.

## Why Use This?

- You're tired of manually renaming files for hours.
- You want to impress your friends with perfectly formatted filenames.
- You're just a little OCD about file organization. (We get it!)

## Disclaimer

No scripts or dragons were harmed in the making of this tool. Use responsibly, or not — we're not your parents. 🤷‍♂️

## Contribute

Found a bug? Have a cool feature idea? Open a pull request or send us a raven!

Happy Renaming! 🚀
