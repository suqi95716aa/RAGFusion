import pypdf

# 打开PDF文件
with open('./doc/test.pdf', 'rb') as file:
    reader = pypdf.PdfReader(file)

    # 初始化文本内容
    text_content = ""

    # 遍历PDF中的每一页
    for page in reader.pages:
        # 提取文本
        text_content += page.extract_text() + "\n"

# 打印文本内容
print(text_content)