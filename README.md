# YouTube 字幕翻译工具 🎥

一个基于 Streamlit 的 Web 应用，可以自动下载 YouTube 视频的英文字幕并翻译成中文。使用 Google Gemini API 提供高质量的翻译服务。

## 功能特点 ✨

- 支持多种 YouTube 链接格式
- 自动提取视频英文字幕
- 使用 Google Gemini API 进行准确翻译
- 简洁直观的用户界面
- 支持翻译结果下载
- 实时翻译状态显示

## 环境要求 🛠️

- Python 3.10 或更高版本
- Windows 10 操作系统
- 稳定的网络连接

## 安装步骤 📥

1. 克隆项目到本地：
```bash
git clone [项目地址]
cd ytbs_web_python1
```

2. 创建并激活虚拟环境：
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置 Google Gemini API：
- 获取 API 密钥
- 设置环境变量或配置文件

## 使用方法 🚀

1. 启动应用：
```bash
streamlit run app.py
```

2. 在浏览器中访问应用（默认地址：http://localhost:8501）

3. 使用步骤：
   - 输入 YouTube 视频链接
   - 点击"开始翻译"按钮
   - 等待翻译完成
   - 查看或下载翻译结果

## 注意事项 ⚠️

- 仅支持具有英文字幕的 YouTube 视频
- 翻译过程可能需要几分钟，取决于视频长度
- 确保网络连接稳定
- 需要有效的 Google Gemini API 密钥

## 技术栈 💻

- Streamlit：Web 界面框架
- Python：后端逻辑处理
- Google Gemini API：翻译服务
- YouTube API：字幕提取

## 贡献指南 🤝

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证 📄

[许可证类型]

## 联系方式 📧

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- [联系方式] 