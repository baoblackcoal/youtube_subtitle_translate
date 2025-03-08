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
col1, col2, col3 = st.columns([9, 3, 3])
with col1:
    youtube_url = st.text_input(
        "输入视频链接",
        placeholder="https://www.youtube.com/watch?v=GiEsyOyk1m4",
        label_visibility="collapsed"
    )
with col2:
    translate_button = st.button("开始翻译", type="primary", use_container_width=True)

with col3:
    read_checkbox = st.checkbox("朗读", value=True)

    
if translate_button:
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
                        st.download_button(
                            label="下载字幕",
                            data=translation,
                            file_name="subtitle_cn.txt",
                            mime="text/plain",
                            use_container_width=True
                        )

                        if read_checkbox:
                            text = escape_text_for_js(translation)
                            speed_value = speed_options[st.session_state.speed]
                            js_code = f"""
                                <script>
                                    function speak() {{
                                        const utterance = new SpeechSynthesisUtterance("{text}");
                                        utterance.lang = 'zh-CN';
                                        utterance.rate = {speed_value};
                                        window.speechSynthesis.speak(utterance);
                                    }}
                                    speak();
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
            except Exception as e:
                st.error(f"发生错误：{str(e)}")

st.markdown("---")
st.markdown("""#### 设置""")
if read_checkbox:    
    st.session_state.speed = st.selectbox(
        "朗读速度",
        options=list(speed_options.keys()),
        index=4,  # Default to 1.5X
        label_visibility="visible"
    )

# 添加页脚
st.markdown("---")
st.markdown("""
#### 使用说明
1. 输入 YouTube 视频链接
2. 点击开始翻译按钮
3. 等待翻译完成后查看结果

⚠️ 注意：
- 仅支持有英文字幕的 YouTube 视频
- 翻译过程可能需要几分钟，请耐心等待
- 确保视频链接格式正确
""")
st.caption("💡 使用 Google Gemini API 提供翻译服务") 