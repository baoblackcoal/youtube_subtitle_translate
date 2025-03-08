import os
import sys
import subprocess

def run_command(command):
    """执行命令并实时输出结果"""
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            shell=True
        )
        
        # 实时输出命令执行结果
        for line in process.stdout:
            print(line, end='')
            
        # 等待命令执行完成
        process.wait()
        
        if process.returncode != 0:
            print(f"Error: Command '{command}' failed with return code {process.returncode}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error executing command '{command}': {str(e)}")
        sys.exit(1)

def main(video_id=None):
    """
    主函数，可以通过命令行参数或直接传入video_id运行
    """
    # 检查命令行参数
    if video_id is None and len(sys.argv) > 1:
        video_id = sys.argv[1]
    
    if video_id is None:
        print("Usage: python main.py <youtube_url>")
        print("Example: python main.py @GiEsyOyk1m4")
        sys.exit(1)
    
    # 获取YouTube URL
    if video_id.startswith("@"):
        # 如果是视频ID格式，构造完整URL
        video_id = video_id[1:]  # 移除@符号
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    elif video_id.startswith(("http://", "https://")):
        youtube_url = video_id
    else:
        print("Error: Invalid YouTube URL format")
        print("Usage: python main.py @VIDEO_ID")
        print("   or: python main.py https://www.youtube.com/watch?v=VIDEO_ID")
        sys.exit(1)
    
    # 获取脚本所在目录的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 步骤1：下载并转换字幕
    download_script = os.path.join(current_dir, "step1_download", "download_and_convert.py")
    print("\n=== Step 1: Downloading and Converting Subtitles ===")
    print(f"Running: python {download_script} {youtube_url}")
    run_command(f'python "{download_script}" "{youtube_url}"')
    
    # 步骤2：翻译字幕
    translate_script = os.path.join(current_dir, "step2_translate", "translate.py")
    print("\n=== Step 2: Translating Subtitles ===")
    print(f"Running: python {translate_script}")
    run_command(f'python "{translate_script}"')
    
    print("\nAll steps completed successfully!")

if __name__ == "__main__":
    main()
