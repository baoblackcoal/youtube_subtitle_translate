import re
import sys
from pathlib import Path

def convert_vtt_to_txt(vtt_file):
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
    
    # Write to txt file
    txt_file = str(Path(vtt_file).with_suffix('.txt'))
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return txt_file

if __name__ == '__main__':
    vtt_file = "Sarcasm with GPT-4o [GiEsyOyk1m4].en.vtt"
    txt_file = convert_vtt_to_txt(vtt_file)
    print(f"Converted {vtt_file} to {txt_file}") 