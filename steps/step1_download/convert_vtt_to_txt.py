import re
import sys
import os
from pathlib import Path

def convert_vtt_to_txt(vtt_file):
    # Ensure input file exists
    if not os.path.exists(vtt_file):
        print(f"Error: Input file {vtt_file} does not exist")
        sys.exit(1)

    with open(vtt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove WEBVTT header and metadata
    content = re.sub(r'WEBVTT\n.*?\n\n', '', content, flags=re.DOTALL)
    
    # Remove timestamps, alignment and position info
    content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*?\n', '', content)
    
    # Remove HTML-style tags and timestamps
    content = re.sub(r'</?[^>]+>', '', content)
    content = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', content)
    
    # Split into lines and clean up
    lines = content.split('\n')
    seen = set()
    clean_lines = []
    
    for line in lines:
        line = line.strip()
        if line and line not in seen:
            seen.add(line)
            clean_lines.append(line)
    
    # Join lines and clean up extra whitespace
    content = ' '.join(clean_lines)
    # Clean up multiple spaces
    content = re.sub(r'\s+', ' ', content)
    content = content.strip()
    
    # Get the output directory from the input file
    output_dir = os.path.dirname(vtt_file)
    base_name = os.path.splitext(os.path.basename(vtt_file))[0]
    txt_file = os.path.join(output_dir, f"{base_name}.txt")
    
    # Write to txt file
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return txt_file

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python convert_vtt_to_txt.py <vtt_file>")
        sys.exit(1)
    
    vtt_file = sys.argv[1]
    txt_file = convert_vtt_to_txt(vtt_file)
    print(f"Converted {vtt_file} to {txt_file}") 