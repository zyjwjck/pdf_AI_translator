# PDF AI Translator

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[English](README.md) | [中文](README_zh.md)

PDF AI Translator是一个使用大模型API将PDF文件翻译并保存为HTML格式的工具，支持点击复制按钮将翻译结果复制到Word等文档中。

## 功能特点
- 支持PDF文件解析和文本提取
- 使用大模型API进行智能翻译
- 将翻译结果保存为HTML格式，带有复制功能
- 支持翻译进度保存和恢复
- 按10页区间组织翻译结果，便于查看

## 配置说明
1. **api_key**：需要修改config.json中的api_key，替换成自己的大模型API密钥（需要申请）
2. **pdf_path**：需要修改为你需要翻译的PDF文件的绝对路径（仅支持可复制文字的PDF）
3. **pagesize**：每次运行翻译的页数，可根据需要修改
4. **request_interval**：翻译请求之间的间隔，可根据API限制调整
5. **其他配置**：可根据需要调整解析区域、模型参数等

## 环境准备
1. 安装Python环境（如Anaconda）
2. 创建虚拟环境：
   ```bash
   conda create -n PDF_env python=3.12
   ```
3. 激活虚拟环境：
   ```bash
   conda activate PDF_env
   ```
4. 安装依赖库：
   ```bash
   pip install pypdfium2 requests
   ```
   或使用requirements.txt文件：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法
1. 进入项目路径
2. 激活虚拟环境：
   ```bash
   conda activate PDF_env
   ```
3. 运行程序：
   ```bash
   python pdf_translation_program.py
   ```

## 项目结构
- `pdf_translation_program.py`：主程序文件
- `config.json`：配置文件（需自行创建）
- `progress.json`：进度文件，记录当前翻译的页码和段落
- `LICENSE`：Apache-2.0许可证文件
- `README.md`：英文项目说明文件
- `README_zh.md`：中文项目说明文件

## 配置文件示例
```json
{
  "api_key": "你的大模型API密钥",
  "api_url": "大模型API地址",
  "model": "使用的模型名称",
  "system_prompt": "系统提示词",
  "user_prompt_template": "用户提示词模板，{text}将被替换为待翻译文本",
  "pdf_path": "PDF文件绝对路径",
  "output_path": "翻译结果保存路径",
  "parse_region": {
    "min_x_ratio": 0,
    "min_y_ratio": 0
  },
  "pagesize": 3,
  "request_interval": 1
}
```

## 许可证
本项目采用Apache-2.0许可证开源，详见[LICENSE](LICENSE)文件。

## 贡献
欢迎提交Issue和Pull Request来改进本项目。

## 注意事项
- 仅支持可复制文字的PDF文件
- 需要有效的大模型API密钥
- 翻译速度取决于API响应速度和网络状况
- 建议根据API限制调整request_interval参数

## 项目地址
[https://github.com/zyjwjck/pdf_AI_translator](https://github.com/zyjwjck/pdf_AI_translator)