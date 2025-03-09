import sys
import os
import subprocess
from convert_vtt_to_txt import convert_vtt_to_txt

def download_subtitles(url):
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)

    # delete all files in the output directory
    for file in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, file))
    
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
        return None
    
    vtt_file = os.path.join(output_dir, 'sub.en.vtt')
    if os.path.exists(vtt_file):
        print(f"Subtitles downloaded successfully to: {vtt_file}")
        return vtt_file
    else:
        print("Failed to download subtitles")
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python download_and_convert.py [YouTube URL]")
        sys.exit(1)
    
    url = sys.argv[1]
    
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