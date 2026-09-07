---
title: "2026-09-06 AI 知识库日报"
date: 2026-09-06T06:00:00+08:00
tags: [AI知识库, daily]
summary: "AI 对话知识提炼:共 1 条对话,提炼 1 条"
---

> 由本机 AI 自动总结,数据来源:当日 AI 对话记录(1/1 条有效)。
> 信息来源分布:Roo Code (本地)(1条)

## 今日知识要点

### 爬虫脚本编写
- **核心结论**: 从指定网站爬取植物页面上的图片，并根据许可协议下载。
- **关键要点**:
  - 网站结构分析: 每个植物页面包含多个 `<figure>` 标签，每个标签内有 `<img>` 标签，包含 `src`, `alt`, `data-caption`, `data-attrib`, `data-license` 等属性。
  - 详细页面结构: 每个植物页面的 `<figure>` 标签中，`data-license` 属性用于判断图片的许可协议。
  - 下载图片: 选择许可协议为 CC0, CC BY 2.0/3.0/4.0, CC BY-SA 的图片，并下载。
  - 图片处理: 下载后将图片转换为 webp 格式。
- **信息来源**: Roo Code (本地)

```python
import requests
from bs4 import BeautifulSoup
import os

url = "https://plants.ces.ncsu.edu/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 获取植物页面列表
plant_pages = soup.find_all('a', class_='plant-link')

for plant_page in plant_pages:
    plant_url = plant_page['href']
    plant_response = requests.get(plant_url)
    plant_soup = BeautifulSoup(plant_response.text, 'html.parser')

    # 获取图片信息
    images = plant_soup.find_all('figure', class_='figure')
    for image in images:
        img_url = image.find('img')['src']
        license = image.get('data-license')
        if license in ['CC BY 4.0', 'CC BY-SA 4.0', 'CC BY 2.0', 'CC BY 3.0', 'CC BY 4.0']:
            img_response = requests.get(img_url)
            with open(f'./assets/{plant_page.text}.webp', 'wb') as f:
                f.write(img_response.content)
```
- **信息来源**: Roo Code (本地)

### 图片下载与转换
- **核心结论**: 根据许可协议下载植物图片，并转换为 webp 格式。
- **关键要点**:
  - 图片下载: 使用 `requests` 库下载图片。
  - 图片转换: 使用 `Pillow` 库将下载的图片转换为 webp 格式。
- **信息来源**: Roo Code (本地)

```python
from PIL import Image

# 图片下载
img_response = requests.get(img_url)
with open(f'./assets/{plant_page.text}.jpg', 'wb') as f:
    f.write(img_response.content)

# 图片转换
img = Image.open(f'./assets/{plant_page.text}.jpg')
img.save(f'./assets/{plant_page.text}.webp', 'webp')
```
- **信息来源**: Roo Code (本地)


---

*本页由 [summarize.py](https://github.com/zhaiming86326/my-blog) 自动生成*
