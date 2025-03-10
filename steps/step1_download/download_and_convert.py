import sys
import os
import subprocess
import json
from convert_vtt_to_txt import convert_vtt_to_txt
from urllib.parse import urlparse, parse_qs

def is_valid_youtube_url(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.netloc not in ['www.youtube.com', 'youtube.com', 'youtu.be']:
            return False
        if parsed_url.path == '/watch':
            query = parse_qs(parsed_url.query)
            return 'v' in query
        return parsed_url.path.startswith('/v/')
    except:
        return False


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


def download_subtitles(url):
    if not is_valid_youtube_url(url):
        print(f"Error: Invalid YouTube URL: {url}")
        return None

    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)

    # delete all files in the output directory
    for file in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, file))

    # First get video title
    video_title = get_video_title(output_dir, url)
    if not video_title:
        print("Failed to get video title")
        return None
    
    print(f"\nAttempting to download subtitles for: {url}")
    print(f"Output directory: {output_dir}")
    
    # Try downloading with auto-generated subtitles
    cmd = [
        'yt-dlp',
        '--skip-download',
        '--write-auto-sub',
        '--sub-lang', 'en',
        '--paths', output_dir,
        '--output', 'sub',
        '--verbose',
        url
    ]
    
    print("\nAttempting to download auto-generated subtitles...")
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        print("\nCommand output:")
        print(result.stdout)
        print("\nCommand errors/warnings:")
        print(result.stderr)
        
        vtt_file = os.path.join(output_dir, 'sub.en.vtt')
        if os.path.exists(vtt_file):
            print(f"\nSubtitles downloaded successfully to: {vtt_file}")
            return vtt_file
    except subprocess.CalledProcessError as e:
        print(f"\nError running auto-generated subtitles command: {str(e)}")
        print("Command output:")
        print(e.stdout)
        print("Command errors:")
        print(e.stderr)
    except Exception as e:
        print(f"\nUnexpected error running auto-generated subtitles command: {str(e)}")
    
    # If auto-generated subtitles failed, try manual subtitles
    cmd = [
        'yt-dlp',
        '--skip-download',
        '--write-sub',
        '--sub-lang', 'en',
        '--paths', output_dir,
        '--output', 'sub',
        '--verbose',
        url
    ]
    
    print("\nAttempting to download manual subtitles...")
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        print("\nCommand output:")
        print(result.stdout)
        print("\nCommand errors/warnings:")
        print(result.stderr)
        
        vtt_file = os.path.join(output_dir, 'sub.en.vtt')
        if os.path.exists(vtt_file):
            print(f"\nSubtitles downloaded successfully to: {vtt_file}")
            return vtt_file
    except subprocess.CalledProcessError as e:
        print(f"\nError running manual subtitles command: {str(e)}")
        print("Command output:")
        print(e.stdout)
        print("Command errors:")
        print(e.stderr)
    except Exception as e:
        print(f"\nUnexpected error running manual subtitles command: {str(e)}")
    
    print("\nFailed to download subtitles - no VTT file found")
    # Check if any other subtitle files were created
    files = os.listdir(output_dir)
    if files:
        print("Files in output directory:", files)
    return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python download_and_convert.py [YouTube URL]")
        print("Example: python download_and_convert.py https://www.youtube.com/watch?v=VIDEO_ID")
        sys.exit(1)
    
    url = sys.argv[1].strip('"\'')  # Remove any quotes from the URL
    
    # Download subtitles
    vtt_file = download_subtitles(url)
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