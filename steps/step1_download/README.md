# YouTube Subtitle Downloader and Converter

A simple tool to download YouTube video subtitles and convert them to plain text format.

## Prerequisites

- Python 3.x
- yt-dlp

## Usage

```bash
python download_and_convert.py "YOUTUBE_URL"
```

Example:
```bash
python download_and_convert.py "https://www.youtube.com/watch?v=GiEsyOyk1m4"
```

## Output

- Downloads subtitle file to: `output/sub.en.vtt`
- Converts to text file at: `output/sub.en.txt`

## Features

- Downloads English auto-generated subtitles from YouTube videos
- Removes timestamps and formatting
- Removes duplicate lines
- Converts to clean, readable text format

## Files

- `download_and_convert.py`: Main script to download and convert subtitles
- `convert_vtt_to_txt.py`: VTT to TXT converter utility 