import sys
import os
import subprocess

def download_subtitles(url):
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepare the yt-dlp command
    cmd = [
        'yt-dlp',
        '--skip-download',
        '--write-auto-sub',
        '--sub-lang', 'en',
        '--paths', output_dir,
        '--output', 'sub',
        url
    ]
    
    print(f"Downloading subtitles from: {url}")
    print(f"Output directory: {output_dir}")
    
    # Run the command
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error downloading subtitles:")
        print(result.stderr)
        sys.exit(1)
    
    vtt_file = os.path.join(output_dir, 'sub.en.vtt')
    if os.path.exists(vtt_file):
        print(f"Subtitles downloaded successfully to: {vtt_file}")
        return vtt_file
    else:
        print("Failed to download subtitles")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python download_subs.py [YouTube URL]")
        sys.exit(1)
    
    download_subtitles(sys.argv[1]) 