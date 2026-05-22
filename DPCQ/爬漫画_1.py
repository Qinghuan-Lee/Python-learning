import requests
import os
import time
from PIL import Image
from io import BytesIO

BASE_DIR = "斗破苍穹"
IMG_DIR = os.path.join(BASE_DIR, "images")
PDF_DIR = os.path.join(BASE_DIR, "pdf")

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

MANGA_CODE = "doupocangqiong140"

session = requests.Session()

# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
#     "Referer": "https://m.happymh.com/",
#     "Origin": "https://m.happymh.com",
#     "Accept": "application/json, text/plain, */*",
#     "X-Requested-With": "XMLHttpRequest"
# }

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://m.happymh.com/",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1"
}

session.headers.update(HEADERS)


def warm_up():
    """关键：先访问页面拿 cookie"""
    url = f"https://m.happymh.com/manga/{MANGA_CODE}.html"
    r = session.get(url, timeout=10)
    r.raise_for_status()


def fetch_all_chapters():
    print("📚 正在获取章节列表...")
    chapters = []
    page = 1

    while True:
        url = (
            "https://m.happymh.com/v2.0/apis/manga/chapterByPage"
            f"?code={MANGA_CODE}&page={page}&order=desc&lang=cn"
        )
        r = session.get(url, timeout=10)
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
    r = session.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    return [img["url"] for img in data["data"]["scans"]]


def images_to_pdf(image_urls, pdf_path):
    images = []
    for url in image_urls:
        img_data = session.get(url, timeout=15).content
        img = Image.open(BytesIO(img_data)).convert("RGB")
        images.append(img)

    images[0].save(pdf_path, save_all=True, append_images=images[1:])


def main():
    warm_up()  # ⭐⭐⭐ 必须

    chapters = fetch_all_chapters()

    for idx, ch in enumerate(chapters, 1):
        title = ch["chapterName"]
        code = ch["codes"]
        name = f"{idx:04d}_{title}"

        print(f"📖 {name}")

        pdf_path = os.path.join(PDF_DIR, f"{name}.pdf")
        if os.path.exists(pdf_path):
            continue

        urls = fetch_chapter_images(code)
        images_to_pdf(urls, pdf_path)
        time.sleep(1)

    print("🎉 全部下载完成")


if __name__ == "__main__":
    main()
