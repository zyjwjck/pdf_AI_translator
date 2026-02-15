import pypdfium2
import json
import requests
import time

# 加载配置文件
def load_config():
    with open('.\config1.json', 'r', encoding='utf-8') as f:
        return json.load(f)
def load_suggest_config():
    with open('.\config.json', 'r', encoding='utf-8') as f:
        return json.load(f)
# 加载进度文件
def load_progress():
    try:
        with open('.\progress.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"current_page": 0}

# 保存进度文件
def save_progress(progress):
    with open('.\progress.json', 'w') as f:
        json.dump(progress, f)

# 解析 PDF 文件的某一页
def parse_pdf_page(pdf_path, page_num, config):
    pdf = pypdfium2.PdfDocument(pdf_path)
    page = pdf.get_page(page_num)
    textpage = page.get_textpage()
    regions = textpage.get_text_bounded(
        left=config["parse_region"]["min_x_ratio"] * page.get_width(),
        bottom=config["parse_region"]["min_y_ratio"] * page.get_height(),
        right=page.get_width(),
        top=page.get_height()
    )
    text = ''.join(regions)
    paragraphs = text.split('\n')  # 简单按空行划分段落
    return "".join(paragraphs)

# 调用大模型进行翻译
def translate_text(config, text):
    time.sleep(1)
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }
    data = {
        "model": config["model"],
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": config["system_prompt"]
            },
            {
                "role": "user",
                "content": config["user_prompt_template"].format(text)
            }
        ]
    }
    try:
        response = requests.post(config["api_url"], headers=headers, json=data, timeout=700)  # 最大等待 10 分钟
        result = response.json()
        translation = result['choices'][0]['message']['content']
        return translation
    except Exception as e:
        print(f"请求大模型出错: {e}")
        return None

# 将翻译结果保存到 HTML 文件
def save_to_html(output_path, page_num, translation):
    paragraphs = translation.split("<Br>换行</Br>")

    with open(output_path, 'a', encoding='utf-8') as f:
        current_time = time.strftime("%Y-%m-%d %H:%M")
        # 计算所属的 10 页区间分块
        start_range = (page_num - 1) // 10 * 10 + 1
        end_range = start_range + 9
        range_str = f"{start_range}-{end_range} 页 {current_time} ————————————————"
        # 检查是否需要添加新的分类展开折叠
        if page_num % 10 == 1:
            f.write(f'<details><summary><h1>{range_str}</h1></summary>')
        f.write(f"<h3>{page_num} 页 - {current_time}</h3><details><summary>展开查看</summary>")
        for i, para in enumerate(paragraphs):
            f.write(f'<p style="color: black; font-family: SimSun; font-size: 10.5pt;" id="para-{page_num}-{i + 1}">{para}</p>')
            f.write(f'<button onclick="copyText(\'para-{page_num}-{i + 1}\')">复制</button>')
            f.write('<script>function copyText(id) { var copyText = document.getElementById(id); var textArea = document.createElement("textarea"); textArea.value = copyText.textContent; document.body.appendChild(textArea); textArea.select(); document.execCommand("Copy"); document.body.removeChild(textArea); }</script>')
        f.write("</details>")
        if page_num % 10 == 0:
            f.write('</details>')

# 主函数
def main():
    config = load_config()
    config1 = load_suggest_config()
    progress = load_progress()
    start_page = progress["current_page"]
    end_page = min(start_page + config["pagesize"], 450)  # 假设 PDF 约 450 页
    for page_num in range(start_page, end_page):
        print(f"正在翻译第 {page_num + 1} 页")
        # 传入 config 参数
        text = parse_pdf_page(config["pdf_path"], page_num, config)
        print(f"即将发起的请求内容（第 {page_num + 1} 页）: {text}")
        translation = translate_text(config, text)
        text1= "\n 英文原文为：【"+text+"】。。。\n 中文翻译初稿为：【"+translation+"】。请你帮忙评审，针对潜在的问题，提出修正或优化意见。\n"
        translation1 = translate_text(config1, text1)
        if translation  and translation1:
            result=translation + "<br/><br/>—————————以下是点评————————<br/>" +translation1
            print(f"大模型返回的翻译结果（第 {page_num + 1} 页）: {result}")
            save_to_html(config["output_path"], page_num + 1, result)
        elif translation  and not translation1:
            result=translation + "<br/><br/>—————————无点评————————<br/>"
            print(f"大模型返回的翻译结果（第 {page_num + 1} 页）: {result}")
            save_to_html(config["output_path"], page_num + 1, result)    
        else:
            print(f"***警告：第 {page_num + 1} 页大模型输出为空*******************************\n")
        progress["current_page"] = page_num + 1
        save_progress(progress)
        time.sleep(config["request_interval"])

if __name__ == "__main__":
    main()