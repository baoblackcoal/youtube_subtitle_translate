import streamlit as st
import subprocess
import os
import re

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

def read_original_text():
    try:
        with open('steps/step1_download/output/sub.en.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None

def ensure_output_directories():
    os.makedirs('steps/step1_download/output', exist_ok=True)
    os.makedirs('steps/step2_translate/output', exist_ok=True)

st.set_page_config(
    page_title="YouTube 字幕翻译工具",
    page_icon="🎥",
    layout="wide"
)

st.title("YouTube 字幕翻译工具 🎥")

st.markdown("""
### 使用说明
1. 输入 YouTube 视频链接
2. 点击开始翻译按钮
3. 等待翻译完成后查看结果

⚠️ 注意：
- 仅支持有英文字幕的 YouTube 视频
- 翻译过程可能需要几分钟，请耐心等待
- 确保视频链接格式正确
""")

# 输入 YouTube URL
youtube_url = st.text_input("请输入 YouTube 视频链接：", 
                           placeholder="https://www.youtube.com/watch?v=...")

# 添加示例链接
st.markdown("示例链接格式：")
st.code("https://www.youtube.com/watch?v=GiEsyOyk1m4")
st.code("https://youtu.be/GiEsyOyk1m4")

if st.button("开始翻译", type="primary"):
    if not youtube_url:
        st.error("请输入有效的 YouTube 链接！")
    elif not is_valid_youtube_url(youtube_url):
        st.error("请输入正确格式的 YouTube 链接！")
    else:
        # 确保输出目录存在
        ensure_output_directories()
        
        with st.spinner("正在下载并翻译字幕，请稍候..."):
            try:
                # 执行翻译脚本
                result = subprocess.run(
                    ['python', 'steps/main.py', youtube_url],
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                
                if result.returncode == 0:
                    st.success("翻译完成！")
                    
                    # 创建两列显示原文和译文
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("英文原文")
                        original_text = read_original_text()
                        if original_text:
                            st.text_area("", value=original_text, height=500, disabled=True)
                        else:
                            st.warning("未找到英文原文，可能该视频没有英文字幕")
                    
                    with col2:
                        st.subheader("中文译文")
                        translation = read_translation_result()
                        if translation:
                            st.text_area("", value=translation, height=500, disabled=True)
                        else:
                            st.warning("翻译失败，请检查网络连接或重试")
                else:
                    error_msg = result.stderr.strip()
                    if "No subtitles available" in error_msg:
                        st.error("该视频没有可用的英文字幕！")
                    else:
                        st.error(f"翻译过程出错：\n{error_msg}")
            except Exception as e:
                st.error(f"发生错误：{str(e)}")

# 添加页脚
st.markdown("---")
st.markdown("💡 本工具使用 Google Gemini API 进行翻译")
st.markdown("📝 支持自动生成的字幕和手动上传的字幕") 