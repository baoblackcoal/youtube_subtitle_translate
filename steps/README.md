# YouTube 字幕下载和翻译工具

这是一个自动化工具，可以下载 YouTube 视频的英文字幕并将其翻译成中文。

## 功能流程

1. 下载 YouTube 视频的英文字幕并转换格式
2. 使用 Google Gemini API 将英文字幕翻译成中文

## 使用方法

运行主脚本并提供 YouTube 视频 ID：

```bash
python main.py @VIDEO_ID
```

例如：
```bash
python main.py @GiEsyOyk1m4
```

## 输出文件

- 英文字幕：`step1_download/output/sub.en.txt`
- 中文字幕：`step2_translate/output/sub.cn.txt`

## 目录结构

- `main.py` - 主脚本
- `step1_download/` - 字幕下载和转换模块
- `step2_translate/` - 字幕翻译模块

## 依赖要求

请确保已安装各个模块所需的依赖：
- `step1_download/requirements.txt`
- `step2_translate/requirements.txt`

## 错误处理

- 如果任何步骤失败，脚本会显示错误信息并退出
- 每个步骤的详细错误处理请参考相应模块的 README 