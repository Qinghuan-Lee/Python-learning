import os
import time
import json
import re
import random
from PIL import Image
from io import BytesIO
from DrissionPage import ChromiumPage

# --- 配置区域 ---
BASE_DIR = "斗破苍穹"
PDF_DIR = os.path.join(BASE_DIR, "pdf")
CACHE_FILE = os.path.join(BASE_DIR, "chapters_cache.json")
MANGA_CODE = "doupocangqiong140"

# 关键参数：每下多少话进行大休息
BATCH_SIZE = 5 

os.makedirs(PDF_DIR, exist_ok=True)

# 初始化浏览器
page = ChromiumPage()

def get_json_data():
    """从页面提取 JSON 文本"""
    time.sleep(1.5) # 给浏览器渲染文本的时间
    raw_text = page.run_js('return document.documentElement.innerText;')
    try:
        if raw_text and '{' in raw_text:
            start_idx = raw_text.find('{')
            end_idx = raw_text.rfind('}') + 1
            json_str = raw_text[start_idx:end_idx]
            return json.loads(json_str)
    except:
        return None

def warm_up():
    print(f"🚀 正在初始化环境...")
    page.get(f"https://m.happymh.com/manga/{MANGA_CODE}.html")
    time.sleep(3)

def fetch_all_chapters():
    """获取章节列表（带本地缓存）"""
    if os.path.exists(CACHE_FILE):
        print(f"📂 发现本地目录缓存，直接读取...")
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    print("📚 正在从网络抓取目录...")
    chapters = []
    page_num = 1
    seen_ids = set()

    while True:
        url = f"https://m.happymh.com/v2.0/apis/manga/chapterByPage?code={MANGA_CODE}&page={page_num}&order=desc&lang=cn"
        page.get(url)
        time.sleep(random.uniform(2, 3))
        
        data_res = get_json_data()
        if not data_res:
            print("❌ 目录获取受阻，请检查浏览器是否需要手动过盾")
            break

        data_body = data_res.get("data", {})
        items = data_body.get("items", [])
        if not items: break

        new_count = 0
        for item in items:
            if item["id"] not in seen_ids:
                chapters.append(item)
                seen_ids.add(item["id"])
                new_count += 1
        
        if new_count == 0 or data_body.get("isEnd") == 1: break
        page_num += 1

    result = chapters[::-1]
    if result:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
    return result

def fetch_chapter_images(chapter_code):
    """访问阅读页过盾并获取图片 API"""
    read_url = f"https://m.happymh.com/manga/read/{MANGA_CODE}/{chapter_code}"
    page.get(read_url)
    
    # 模拟等待过盾
    for _ in range(10):
        if "cf-challenge" in page.html or "Checking your browser" in page.html:
            print("🛡️ 检测到 Cloudflare 盾，请在浏览器中手动点击验证...")
            time.sleep(5)
        else:
            break
            
    api_url = f"https://m.happymh.com/v2.0/apis/manga/reading?code={chapter_code}"
    page.get(api_url)
    data = get_json_data()
    if data and "data" in data:
        return [img["url"] for img in data["data"]["scans"]]
    return []

def images_to_pdf(image_urls, pdf_path, chapter_code):
    """下载图片并合成 PDF"""
    images = []
    # 动态设置每章的 Referer
    page.set.headers({'Referer': f'https://m.happymh.com/manga/read/{MANGA_CODE}/{chapter_code}'})
    
    for i, url in enumerate(image_urls):
        try:
            resp = page.get(url)
            if resp.status_code == 200:
                img = Image.open(BytesIO(resp.content)).convert("RGB")
                images.append(img)
            # 图片间短暂停顿
            time.sleep(random.uniform(0.3, 0.7))
        except Exception as e:
            print(f"   ⚠️ 图片下载异常: {e}")

    if images:
        images[0].save(pdf_path, save_all=True, append_images=images[1:])
        return True
    return False

def main():
    try:
        warm_up()
        chapters = fetch_all_chapters()
        
        downloaded_in_session = 0

        for idx, ch in enumerate(chapters, 1):
            title = ch["chapterName"]
            code = ch["codes"]
            safe_title = "".join([c for c in title if c not in r'\/:*?"<>|']).strip()
            name = f"{idx:04d}_{safe_title}"
            pdf_path = os.path.join(PDF_DIR, f"{name}.pdf")

            if os.path.exists(pdf_path):
                continue

            print(f"📖 [{idx}/{len(chapters)}] 正在处理: {name}")
            
            urls = fetch_chapter_images(code)
            if urls and images_to_pdf(urls, pdf_path, code):
                print(f"   ✅ 完成")
                downloaded_in_session += 1
            else:
                print(f"   ❌ 失败：未获取到数据，建议更换 IP 后重试")
                time.sleep(10) # 失败了多歇会
                continue

            # --- 延迟挂机策略 ---
            if downloaded_in_session % BATCH_SIZE == 0:
                rest_time = random.uniform(60, 120)
                print(f"☕ 已连续下载 {BATCH_SIZE} 话，大休息中，防止封锁... ({int(rest_time)}秒)")
                time.sleep(rest_time)
            else:
                rest_time = random.uniform(10, 20)
                print(f"🕒 章节间小憩 {int(rest_time)} 秒...")
                time.sleep(rest_time)

    except KeyboardInterrupt:
        print("\n👋 用户手动停止")
    finally:
        print("🏁 程序运行结束，已存入 PDF 文件夹。")

if __name__ == "__main__":
    main()