import asyncio
import websockets
import json
import re
import subprocess
import os
from PIL import Image
import time

NAPCAT_WS = "ws://127.0.0.1:6700"
ACCESS_TOKEN = "123456"

JM_EXE_PATH = r"C:\Users\26272\AppData\Roaming\Python\Python313\Scripts\jmcomic.exe"
JM_OUTPUT_DIR = r"D:\JMComic"

async def handle_message(ws, data):
    if data.get("post_type") != "message" or data.get("message_type") != "group":
        return

    group_id = data["group_id"]
    message = data["raw_message"].strip()

    match = re.match(r"^/jm\s+(\d+)$", message)
    if not match:
        return

    jm_id = match.group(1)
    print(f"📩 收到指令: /jm {jm_id} 来自群 {group_id}")

    # 先检查本地是否已有对应PDF
    pdf_path = os.path.join(JM_OUTPUT_DIR, f"{jm_id}.pdf")
    if os.path.exists(pdf_path):
        print("📂 已存在 PDF，直接发送")
        await send_group_msg(ws, group_id, f"📚 检测到本地已存在 {jm_id}.pdf，直接发送中...")
        await upload_group_file(ws, group_id, pdf_path)
        await send_group_msg(ws, group_id, f"✅ 已发送 {jm_id}.pdf")
        return

    # 没有PDF则检查是否存在文件夹
    existing_folder = find_existing_folder(jm_id)
    if existing_folder:
        print(f"📂 找到已有文件夹：{existing_folder}")
        await send_group_msg(ws, group_id, f"📁 已存在本子文件夹，正在生成 PDF...")
        success = images_to_pdf(existing_folder, pdf_path)
        if success:
            await upload_group_file(ws, group_id, pdf_path)
            await send_group_msg(ws, group_id, f"✅ 已生成并发送 {jm_id}.pdf！")
        else:
            await send_group_msg(ws, group_id, f"❌ PDF 生成失败: {existing_folder}")
        return

    # 若本地完全没有 → 执行下载
    await send_group_msg(ws, group_id, f"🔍 未找到 {jm_id}，开始下载禁漫本子，请稍候...")

    try:
        # 记录下载前文件夹情况
        before = set(f for f in os.listdir(JM_OUTPUT_DIR) if os.path.isdir(os.path.join(JM_OUTPUT_DIR, f)))

        subprocess.run([JM_EXE_PATH, jm_id], check=True)
        time.sleep(3)

        # 找到新增文件夹
        after = set(f for f in os.listdir(JM_OUTPUT_DIR) if os.path.isdir(os.path.join(JM_OUTPUT_DIR, f)))
        new_folders = after - before

        if not new_folders:
            await send_group_msg(ws, group_id, "❌ 未找到新生成的本子文件夹（可能已存在或下载失败）")
            return

        latest_folder = max(
            [os.path.join(JM_OUTPUT_DIR, f) for f in new_folders],
            key=lambda p: os.path.getmtime(p),
        )

        print(f"✅ 新下载的文件夹：{latest_folder}")

        success = images_to_pdf(latest_folder, pdf_path)
        if success:
            await upload_group_file(ws, group_id, pdf_path)
            await send_group_msg(ws, group_id, f"✅ 本子 {jm_id} 已生成并发送！")
        else:
            await send_group_msg(ws, group_id, f"❌ 图片合成失败: {latest_folder}")

    except Exception as e:
        await send_group_msg(ws, group_id, f"❌ 生成失败: {e}")
        print("错误:", e)

def find_existing_folder(jm_id):
    """尝试在输出目录中找到包含该本子的文件夹"""
    for f in os.listdir(JM_OUTPUT_DIR):
        full_path = os.path.join(JM_OUTPUT_DIR, f)
        if os.path.isdir(full_path):
            # 检查文件夹内有无编号对应的 json 或命名规则
            for inner_file in os.listdir(full_path):
                if jm_id in inner_file:
                    return full_path
    return None

def images_to_pdf(folder, pdf_path):
    """将文件夹内所有图片合成为 PDF"""
    try:
        images = []
        for f in sorted(os.listdir(folder)):
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                img = Image.open(os.path.join(folder, f)).convert("RGB")
                images.append(img)
        if not images:
            return Falsex
        images[0].save(pdf_path, save_all=True, append_images=images[1:])
        return True
    except Exception as e:
        print("PDF 生成出错:", e)
        return False

async def send_group_msg(ws, group_id, text):
    payload = {
        "action": "send_group_msg",
        "params": {"group_id": group_id, "message": text},
        "echo": "send_msg"
    }
    await ws.send(json.dumps(payload))

async def upload_group_file(ws, group_id, file_path):
    payload = {
        "action": "upload_group_file",
        "params": {
            "group_id": group_id,
            "file": file_path,
            "name": os.path.basename(file_path)
        },
        "echo": "upload_file"
    }
    await ws.send(json.dumps(payload))

async def main():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    async with websockets.connect(NAPCAT_WS, additional_headers=headers) as ws:
        print("✅ 已连接 NapCat WebSocket，开始监听群消息...")
        async for msg in ws:
            try:
                data = json.loads(msg)
                await handle_message(ws, data)
            except Exception as e:
                print("⚠️ 消息处理异常：", e)

if __name__ == "__main__":
    asyncio.run(main())
