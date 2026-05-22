import requests
import os
import time
import cloudscraper  # 需要先执行 pip install cloudscraper
from PIL import Image
from io import BytesIO

# --- 配置区域 ---
BASE_DIR = "斗破苍穹"
IMG_DIR = os.path.join(BASE_DIR, "images")
PDF_DIR = os.path.join(BASE_DIR, "pdf")
MANGA_CODE = "doupocangqiong140"

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

# 初始化 cloudscraper (模拟 Chrome 浏览器)
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    }
)

# 更新默认 Headers
HEADERS = {
    "Referer": "https://m.happymh.com/",
    "Origin": "https://m.happymh.com",
    "Accept": "application/json, text/plain, */*",
    "X-Requested-With": "XMLHttpRequest"
}
scraper.headers.update(HEADERS)

def warm_up():
    """通过访问主页获取必要的验证 Cookie"""
    print(f"🚀 正在尝试绕过防护访问主页...")
    url = f"https://m.happymh.com/manga/{MANGA_CODE}.html"
    try:
        r = scraper.get(url, timeout=20)
        r.raise_for_status()
        print("✅ 验证通过")
    except Exception as e:
        print(f"❌ 验证失败，请检查网络或是否需要代理: {e}")
        exit()

def fetch_all_chapters():
    print("📚 正在获取章节列表...")
    chapters = []
    page = 1

    while True:
        url = (
            "https://m.happymh.com/v2.0/apis/manga/chapterByPage"
            f"?code={MANGA_CODE}&page={page}&order=desc&lang=cn"
        )
        r = scraper.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()

        items = data.get("data", [])
        if not items:
            break

        chapters.extend(items)
        page += 1
        time.sleep(0.5)

    print(f"✅ 共获取 {len(chapters)} 话")
    return chapters[::-1]

def fetch_chapter_images(chapter_code):
    url = f"https://m.happymh.com/v2.0/apis/manga/reading?code={chapter_code}"
    r = scraper.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    return [img["url"] for img in data["data"]["scans"]]

def images_to_pdf(image_urls, pdf_path):
    images = []
    print(f"   📥 正在下载图片 (共 {len(image_urls)} 张)...")
    
    for i, url in enumerate(image_urls):
        try:
            # 这里的图片下载也建议使用 scraper
            img_data = scraper.get(url, timeout=20).content
            img = Image.open(BytesIO(img_data)).convert("RGB")
            images.append(img)
            # 频繁请求容易被封 IP，建议加个微小延迟
            if i % 5 == 0:
                time.sleep(0.2)
        except Exception as e:
            print(f"   ⚠️ 第 {i+1} 张图片下载失败: {e}")

    if images:
        images[0].save(pdf_path, save_all=True, append_images=images[1:])
        print(f"   💾 已保存至: {pdf_path}")
    else:
        print(f"   ❌ 该章节无有效图片，跳过保存")

def main():
    # 1. 绕过防护
    warm_up()

    # 2. 获取目录
    chapters = fetch_all_chapters()

    # 3. 循环下载
    for idx, ch in enumerate(chapters, 1):
        title = ch["chapterName"]
        code = ch["codes"]
        name = f"{idx:04d}_{title}".replace("/", " ").replace("\\", " ") # 防止文件名非法字符

        pdf_path = os.path.join(PDF_DIR, f"{name}.pdf")
        
        # 跳过已存在的
        if os.path.exists(pdf_path):
            print(f"⏩ 跳过已存在: {name}")
            continue

        print(f"📖 正在处理: {name}")
        try:
            urls = fetch_chapter_images(code)
            images_to_pdf(urls, pdf_path)
            # 章节间停顿，模拟真人阅读
            time.sleep(1.5)
        except Exception as e:
            print(f"❌ 处理章节 {name} 时出错: {e}")

    print("🎉 全部任务处理完成")

if __name__ == "__main__":
    main()