# 字幕翻译工具

这是一个使用 Google Gemini API 将英文字幕翻译成中文的简单工具。

## 功能特点

- 支持英文到中文的文本翻译
- 使用 Google Gemini 2.0 Flash 模型进行翻译
- 保持原文的格式和换行
- 支持代理设置

## 依赖要求

- Python 3.6+
- requests==2.31.0

## 配置说明

在运行脚本之前，需要设置以下配置：

1. Gemini API 密钥
2. 代理设置（如果需要）

这些配置已在 `translate.py` 文件中设置：

```python
# 配置API密钥
API_KEY = "YOUR_API_KEY"

# 设置代理
os.environ['HTTP_PROXY'] = 'http://your.proxy:port'
os.environ['HTTPS_PROXY'] = 'http://your.proxy:port'
```

## 使用方法

1. 确保输入文件位于正确位置：`../step1_download/output/sub.en.txt`

2. 运行翻译脚本：
   ```bash
   python translate.py
   ```

3. 翻译完成后，可以在 `output/sub.cn.txt` 中找到翻译结果

## 输入/输出

- 输入文件：`../step1_download/output/sub.en.txt`
- 输出文件：`output/sub.cn.txt`

## 错误处理

脚本包含以下错误处理：

- 检查输入文件是否存在
- 处理 API 请求错误
- 处理文件读写错误

如果遇到任何错误，脚本会打印错误信息并退出。 