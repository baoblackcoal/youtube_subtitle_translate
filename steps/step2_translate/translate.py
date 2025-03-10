import os
import sys
import requests
import json
import time

# 设置代理
# os.environ['HTTP_PROXY'] = 'http://192.168.1.16:10811'
# os.environ['HTTPS_PROXY'] = 'http://192.168.1.16:10811'

# 配置API密钥
API_KEY = "AIzaSyAWCkwGlec6ECgm_r5PkQxEJjqFEs8E36o"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def read_file(file_path):
    """读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        sys.exit(1)

def write_file(file_path, content):
    """写入文件内容"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing file {file_path}: {str(e)}")
        sys.exit(1)

def translate_text(text):
    """使用Gemini翻译文本"""
    try:
        # 创建请求数据
        data = {
            "contents": [{
                "parts":[{
                    "text": f"""
Please summarize and translate the following <source_text></source_text> text to Simplified Chinese. 

Output format requirements:
1. Only provide the translation, no explanations.
2. output format must be like <output></output>.

Summary requirements:
1. summary_title should be concise and to the point.
2. summary_content should be concise and to the point, no more than 100 words.
3. summary_highlights should be 5~10 sentences, with numbers in the beginning of each sentence, highlight the main points of the text.

Translation requirements:
1. Add punctuation and paragraph breaks to make the content easier to read. 

<output>
summary_title
summary_content
summary_highlights
translation_content
</output>

<source_text>
{text}
</source_text>
"""
                }]
            }]
        }
        
        # 设置代理
        proxies = {
            'http': 'http://192.168.1.16:10811',
            'https': 'http://192.168.1.16:10811'
        }
        
        # 发送请求
        headers = {'Content-Type': 'application/json'}
        # response = requests.post(API_URL, headers=headers, json=data, proxies=proxies)
        response = requests.post(API_URL, headers=headers, json=data)
        
        # 检查响应状态
        response.raise_for_status()
        
        # 解析响应
        result = response.json()
        if 'candidates' in result and len(result['candidates']) > 0:
            return result['candidates'][0]['content']['parts'][0]['text'].strip()
        else:
            raise Exception("Empty response from Gemini API")
            
    except Exception as e:
        print(f"Translation error: {str(e)}")
        sys.exit(1)

def main():
    # 获取脚本所在目录的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 设置输入输出路径
    input_file = os.path.normpath(os.path.join(current_dir, "..", "step1_download", "output", "sub.en.txt"))
    output_file = os.path.normpath(os.path.join(current_dir, "output", "sub.cn.txt"))

    # delete all files in the output directory
    output_dir = os.path.dirname(output_file)
    for file in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, file))
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        sys.exit(1)
    
    # 读取英文内容
    print("Reading English subtitles...")
    english_text = read_file(input_file)
    
    # 翻译内容
    print("Translating to Chinese...")
    chinese_text = translate_text(english_text)

    # delete <output> and </output> in the response
    chinese_text = chinese_text.replace("<output>", "").replace("</output>", "")
    # change summary_title to 标题
    chinese_text = chinese_text.replace("summary_title", "标题")
    # change summary_content to 总结
    chinese_text = chinese_text.replace("summary_content", "总结")
    # change summary_highlights to 亮点
    chinese_text = chinese_text.replace("summary_highlights", "亮点")
    # change translation_content to 字幕翻译
    chinese_text = chinese_text.replace("translation_content", "字幕翻译")
    
    # 保存翻译结果
    print("Saving Chinese translation...")
    write_file(output_file, chinese_text)
    
    print("Translation completed successfully!")

if __name__ == "__main__":
    main() 