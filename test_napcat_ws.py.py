import asyncio
import websockets
import json

async def test():
    uri = "ws://127.0.0.1:6700"  # NapCat WebSocket 地址
    headers = {
        "Authorization": "Bearer 123456"  # 如果 napcat 配置里 accessToken 是 123456
    }

    async with websockets.connect(uri, additional_headers=headers) as ws:
        print("✅ 已连接到 NapCat WebSocket!")

        # 发送 OneBot API 测试请求
        payload = {
            "action": "get_login_info",
            "params": {},
            "echo": "test"
        }
        await ws.send(json.dumps(payload))
        print("📤 已发送 get_login_info 请求")

        # 等待响应
        response = await ws.recv()
        print("📥 收到响应：", response)

asyncio.run(test())
