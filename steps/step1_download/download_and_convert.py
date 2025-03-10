import sys
import os
import subprocess
import json
from convert_vtt_to_txt import convert_vtt_to_txt
from urllib.parse import urlparse, parse_qs
import re

def is_valid_youtube_url(url: str) -> bool:
    """
    Check if the given URL is a valid YouTube URL.
    
    Args:
        url (str): The URL to check
        
    Returns:
        bool: True if the URL is a valid YouTube URL, False otherwise
    """
    # YouTube URL patterns
    patterns = [
        r'^https?://(?:www\.)?youtube\.com/watch\?(?=.*v=\w+)(?:\S+)?$',  # Standard YouTube URL
        r'^https?://(?:www\.)?youtube\.com/v/\w+(?:\S+)?$',  # Embedded YouTube URL
        r'^https?://youtu\.be/\w+(?:\S+)?$'  # Short YouTube URL
    ]
    
    return any(re.match(pattern, url) for pattern in patterns)


def get_video_title(output_dir, url):
    title_cmd = [
        'yt-dlp',
        '--skip-download',
        '--get-title',
        url
    ]
    
    title_result = subprocess.run(title_cmd, capture_output=True, text=True)
    if title_result.returncode == 0:
        video_title = title_result.stdout.strip()
        # Save title to a json file
        title_file = os.path.join(output_dir, 'video_info.json')
        with open(title_file, 'w', encoding='utf-8') as f:
            json.dump({'title': video_title}, f, ensure_ascii=False)
        return video_title
    else:
        print(f"Error getting video title: {title_result.stderr}")
        return None


def download_subtitles(output_dir:str, url: str) -> str:
    """
    Download subtitles from a YouTube video URL.
    
    Args:
        url (str): The YouTube video URL.
        
    Returns:
        str: Path to the downloaded subtitle file, or None if download fails.
    """
    if not is_valid_youtube_url(url):
        print("Invalid YouTube URL")
        return None

    try:
        # First try to download manual English subtitles
        print("\nAttempting to download manual English subtitles...")
        command = [
            "yt-dlp",
            "--skip-download",  # Don't download the video
            "--write-sub",  # Write subtitles
            "--sub-lang", "en",  # English subtitles
            "--no-playlist",  # Don't download playlist
            "--paths", output_dir,  # Output directory
            "--output", "sub",  # Output filename
            "--verbose",  # Show detailed progress
            url
        ]
        
        print("Running command:", " ".join(command))
        result = subprocess.run(command, capture_output=True, text=True)
        print("\nCommand output:")
        print(result.stdout)
        
        if result.stderr:
            print("\nCommand errors/warnings:")
            print(result.stderr)

        # If manual subtitles don't exist, try auto-generated ones
        if "Subtitles: en" not in result.stderr and "Subtitles: en" not in result.stdout:
            print("\nAttempting to download auto-generated subtitles...")
            command = [
                "yt-dlp",
                "--skip-download",
                "--write-auto-sub",
                "--sub-lang", "en",
                "--no-playlist",  # Don't download playlist
                "--paths", output_dir,
                "--output", "sub",
                "--verbose",
                url
            ]
            
            print("Running command:", " ".join(command))
            result = subprocess.run(command, capture_output=True, text=True)
            print("\nCommand output:")
            print(result.stdout)
            
            if result.stderr:
                print("\nCommand errors/warnings:")
                print(result.stderr)

        # Check if the subtitle file was created
        vtt_file = os.path.join(output_dir, "sub.en.vtt")
        if os.path.exists(vtt_file):
            print(f"\nSubtitles downloaded successfully to: {vtt_file}")
            return vtt_file
        else:
            print("\nNo subtitles were downloaded")
            return None

    except Exception as e:
        print(f"Error downloading subtitles: {str(e)}")
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python download_and_convert.py [YouTube URL]")
        print("Example: python download_and_convert.py https://www.youtube.com/watch?v=VIDEO_ID")
        sys.exit(1)
    
    url = sys.argv[1].strip('"\'')  # Remove any quotes from the URL    
    
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    # delete all files in the output directory
    for file in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, file))

    print(f"\nAttempting to download subtitles for: {url}")
    print(f"Output directory: {output_dir}")


    # first get video title
    video_title = get_video_title(output_dir, url)
    if not video_title:
        print("Failed to get video title")
        return None
    
    # Download subtitles
    vtt_file = download_subtitles(output_dir, url)
    if not vtt_file:
        sys.exit(1)
    
    # Convert to text
    try:
        txt_file = convert_vtt_to_txt(vtt_file)
        print(f"Successfully converted to: {txt_file}")
    except Exception as e:
        print(f"Error converting subtitles: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 