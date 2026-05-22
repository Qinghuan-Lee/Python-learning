import os
import time
from PIL import Image
from io import BytesIO
from DrissionPage import SessionPage

# --- 配置区域 ---
BASE_DIR = "斗破苍穹"
PDF_DIR = os.path.join(BASE_DIR, "pdf")
MANGA_CODE = "doupocangqiong140"

os.makedirs(PDF_DIR, exist_ok=True)

# 初始化页面对象 (SessionPage 速度快，如果还报403，可改为 ChromiumPage)
page = SessionPage()

# 设置通用 Headers
page.headers.update({
    "Referer": "https://m.happymh.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

def warm_up():
    print(f"🚀 正在通过浏览器环境绕过防护...")
    url = f"https://m.happymh.com/manga/{MANGA_CODE}.html"
    res = page.get(url)
    if res.status_code == 200:
        print("✅ 验证通过")
    else:
        print(f"❌ 依旧被拦截，错误码: {res.status_code}")
        # 如果这里还报错，建议将 SessionPage() 换成 ChromiumPage() 运行一次
        exit()

def fetch_all_chapters():
    print("📚 正在获取章节列表...")
    chapters = []
    page_num = 1
    while True:
        url = f"https://m.happymh.com/v2.0/apis/manga/chapterByPage?code={MANGA_CODE}&page={page_num}&order=desc&lang=cn"
        res = page.get(url)
        data = res.json()
        items = data.get("data", [])
        if not items:
            break
        chapters.extend(items)
        page_num += 1
        time.sleep(0.5)
    print(f"✅ 共获取 {len(chapters)} 话")
    return chapters[::-1]

def fetch_chapter_images(chapter_code):
    url = f"https://m.happymh.com/v2.0/apis/manga/reading?code={chapter_code}"
    res = page.get(url)
    data = res.json()
    return [img["url"] for img in data["data"]["scans"]]

def images_to_pdf(image_urls, pdf_path):
    images = []
    for i, url in enumerate(image_urls):
        try:
            # 下载图片
            img_res = page.get(url)
            img = Image.open(BytesIO(img_res.content)).convert("RGB")
            images.append(img)
            if i % 10 == 0: time.sleep(0.1)
        except Exception as e:
            print(f"   ⚠️ 图片下载失败: {e}")

    if images:
        images[0].save(pdf_path, save_all=True, append_images=images[1:])
        return True
    return False

def main():
    warm_up()
    chapters = fetch_all_chapters()

    for idx, ch in enumerate(chapters, 1):
        title = ch["chapterName"]
        code = ch["codes"]
        # 清理文件名非法字符
        safe_title = "".join([c for c in title if c not in r'\/:*?"<>|'])
        name = f"{idx:04d}_{safe_title}"
        pdf_path = os.path.join(PDF_DIR, f"{name}.pdf")

        if os.path.exists(pdf_path):
            continue

        print(f"📖 正在下载: {name}")
        try:
            urls = fetch_chapter_images(code)
            if images_to_pdf(urls, pdf_path):
                print(f"   ✅ 已保存")
            time.sleep(1) # 避免请求过快
        except Exception as e:
            print(f"   ❌ 章节出错: {e}")

if __name__ == "__main__":
    main()