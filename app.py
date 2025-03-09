import streamlit as st
import subprocess
import os
import re
import json
import logging
from streamlit.components.v1 import html

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def escape_text_for_js(text: str) -> str:
    """Escape text for safe use in JavaScript string."""
    return json.dumps(text)[1:-1]  # Remove the outer quotes that json.dumps adds

def get_video_title() -> str:
    """Get video title from saved info, or return default name if not found."""
    try:
        with open('steps/step1_download/output/video_info.json', 'r', encoding='utf-8') as f:
            info = json.load(f)
            # Clean the title to make it suitable for a filename
            title = info['title']
            # Remove invalid filename characters
            title = re.sub(r'[<>:"/\\|?*]', '', title)
            # Limit length
            title = title[:100]  # Limit to 100 characters
            return title
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return "subtitle"

def is_valid_youtube_url(url):
    # YouTube URL patterns
    patterns = [
        r'^https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',
        r'^https?://youtu\.be/[\w-]+',
        r'^https?://(?:www\.)?youtube\.com/embed/[\w-]+'
    ]
    return any(re.match(pattern, url) for pattern in patterns)

def read_translation_result():
    try:
        with open('steps/step2_translate/output/sub.cn.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None

def ensure_output_directories():
    os.makedirs('steps/step1_download/output', exist_ok=True)
    os.makedirs('steps/step2_translate/output', exist_ok=True)

def get_translation_file():
    try:
        with open('steps/step2_translate/output/sub.cn.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None

st.set_page_config(
    page_title="YouTube 字幕翻译",
    page_icon="🎥",
    layout="centered"
)


speed_options = {
        "0.5X": 0.5,
        "0.75X": 0.75,
        "1X": 1.0,
        "1.25X": 1.25,
        "1.5X": 1.5,
        "2X": 2.0,
        "3X": 3.0,
    }

if 'speed' not in st.session_state:
    st.session_state.speed = "1.5X"


st.markdown("##### YouTube 字幕翻译成中文 🎥")



# 输入 YouTube URL
col1, col2 = st.columns([9, 3])
with col1:
    youtube_url = st.text_input(
        "输入视频链接",
        placeholder="https://www.youtube.com/watch?v=GiEsyOyk1m4",
        label_visibility="collapsed"
    )
with col2:
    translate_button = st.button("开始翻译", type="primary", use_container_width=True)

col3, col4, col5 = st.columns([3, 3, 3])
with col3:
    auto_download_checkbox = st.checkbox("自动下载", value=True)

with col4:
    summary_checkbox = st.checkbox("总结", value=False)
    
    


    
if translate_button:
    # #exec install requests
    # a = subprocess.run(['pip', 'install', 'requests'])
    # st.write(a)

    if not youtube_url:
        youtube_url = "https://www.youtube.com/watch?v=GiEsyOyk1m4"
    
    if not is_valid_youtube_url(youtube_url):
        st.error("无效的视频链接")
    else:
        ensure_output_directories()
        with st.spinner("正在翻译中..."):
            try:
                result = subprocess.run(
                    ['python', 'steps/main.py', youtube_url],
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                
                if result.returncode == 0:
                    translation = read_translation_result()
                    if translation:                        
                        st.text_area(
                            label="译文",
                            value=translation,
                            height=400
                        )
                        st.success("翻译完成")


                        # 提供下载按钮
                        video_title = get_video_title()
                        download_button = st.download_button(
                            label="下载字幕",
                            data=translation,
                            file_name=f"{video_title}.txt",
                            mime="text/plain",
                            use_container_width=True,
                            key="download_button"
                        )

                        if auto_download_checkbox:
                            js_code = """
                            <script>
                                // Wait for the page to fully load
                                window.addEventListener('load', function() {
                                    // Find the download button by its key and click it
                                    const buttons = window.parent.document.querySelectorAll('button');
                                    for (const button of buttons) {
                                        if (button.innerText === '下载字幕') {
                                            button.click();
                                            break;
                                        }
                                    }
                                });
                            </script>
                            """
                            html(js_code)                        
                        
                    else:
                        st.warning("翻译失败，请重试")
                else:
                    error_msg = result.stderr.strip()
                    if "No subtitles available" in error_msg:
                        st.error("该视频没有可用的英文字幕")
                    else:
                        st.error("翻译失败，请确保视频有英文字幕")

                # 在浏览器控制台显示日志
                debug_js = f"""
                    <script>
                        console.group('翻译过程日志');
                        console.log('标准输出:', {json.dumps(result.stdout)});
                        console.log('标准错误:', {json.dumps(result.stderr)});
                        console.log('返回码:', {json.dumps(result.returncode)});
                        console.groupEnd();
                    </script>
                """
                html(debug_js)

            except Exception as e:
                st.error(f"发生错误：{str(e)}")


# st.markdown("---")
# st.markdown("""#### 设置""")


# 添加页脚
st.markdown("---")
st.markdown("""
#### 使用说明
1. 输入 YouTube 视频链接
2. 点击开始翻译按钮
3. 等待翻译完成后查看结果, 如果朗读选项勾选, 则可以听到翻译结果

⚠️ 注意：
- 仅支持有英文字幕的 YouTube 视频
- 翻译过程可能需要几分钟，请耐心等待
- 确保视频链接格式正确
""")
st.caption("💡 使用 Google Gemini API 提供翻译服务") 