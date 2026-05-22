import os
import time
import json
import random
from PIL import Image
from io import BytesIO
from DrissionPage import ChromiumPage, ChromiumOptions

# --- 配置 ---
BASE_DIR = "斗破苍穹"
PDF_DIR = os.path.join(BASE_DIR, "pdf")
CACHE_FILE = os.path.join(BASE_DIR, "chapters_cache.json")
MANGA_CODE = "doupocangqiong140"

os.makedirs(PDF_DIR, exist_ok=True)

# 隐藏驱动特征，防止被 Cloudflare 直接识破
co = ChromiumOptions()
co.set_argument('--disable-blink-features=AutomationControlled')
page = ChromiumPage(co)

def load_chapters():
    if not os.path.exists(CACHE_FILE):
        print(f"❌ 错误：找不到缓存文件 {CACHE_FILE}")
        print("请先运行之前的‘获取目录’脚本，或者手动确保该文件存在。")
        return None
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def download_by_index(index, chapters):
    # 数组索引从0开始，所以输入1对应索引0
    try:
        chapter_data = chapters[index - 1]
    except IndexError:
        print(f"❌ 错误：超出范围！目前只有 1-{len(chapters)} 话。")
        return False

    title = chapter_data['chapterName']
    code = chapter_data['codes']
    url = f"https://m.happymh.com/manga/read/{MANGA_CODE}/{code}"
    
    print(f"\n📖 正在准备下载第 {index} 话: {title}")
    print(f"🔗 URL: {url}")
    
    page.get(url)
    
    # --- 过盾检测 ---
    print("⏳ 正在等待页面加载 (如遇验证码请手动点击)...")
    time.sleep(3)
    while "cf-challenge" in page.html or "Checking your browser" in page.html:
        time.sleep(2)

    # --- 模拟滚动加载 ---
    print("📜 正在滚动页面嗅探图片...")
    for _ in range(10):
        page.scroll.down(1000)
        time.sleep(0.5)

    # --- 提取图片 ---
    img_urls = []
    imgs = page.eles('tag:img')
    for img in imgs:
        src = img.attr('src')
        if src and ('scans' in src or 'happymh' in src) and 'logo' not in src.lower():
            if src not in img_urls:
                img_urls.append(src)

    if len(img_urls) < 3:
        print("❌ 嗅探失败，没找到足够的图片。")
        return False

    # --- 下载并合成 ---
    print(f"✅ 找到 {len(img_urls)} 张图，开始转换 PDF...")
    images = []
    page.set.headers({'Referer': url})
    
    for i, img_url in enumerate(img_urls):
        try:
            resp = page.get(img_url)
            if resp.status_code == 200:
                img = Image.open(BytesIO(resp.content)).convert("RGB")
                images.append(img)
                print(f"\r   下载中: {i+1}/{len(img_urls)}", end="")
        except:
            continue
    
    if images:
        safe_title = "".join([c for c in title if c not in r'\/:*?"<>|']).strip()
        pdf_path = os.path.join(PDF_DIR, f"{index:04d}_{safe_title}.pdf")
        images[0].save(pdf_path, save_all=True, append_images=images[1:])
        print(f"\n✨ 成功！已保存至: {pdf_path}")
        return True
    return False

def main():
    chapters = load_chapters()
    if not chapters: return

    print(f"=== 斗破苍穹 点杀下载器 ===")
    print(f"当前共有 {len(chapters)} 话可用。")

    while True:
        u_input = input("\n请输入话数编号 (如 123，输入 q 退出): ").strip()
        if u_input.lower() == 'q': break
        
        if not u_input.isdigit():
            print("⚠️ 请输入纯数字！")
            continue
        
        target_idx = int(u_input)
        success = download_by_index(target_idx, chapters)
        
        if success:
            print(f"🎉 第 {target_idx} 话处理完毕。")
        else:
            print(f"❌ 第 {target_idx} 话下载失败。")

if __name__ == "__main__":
    main()