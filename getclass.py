import requests
import time
import sys

# =========================
# 1. 基本配置
# =========================

# Clash 代理（你已确认一直开着）
PROXIES = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}

# 超时设置（选课期一定要长）
TIMEOUT = 30

# =========================
# 2. 接口地址（替换成你自己的）
# =========================

# 获取可选课程列表接口（kxkc）
KXKC_URL = "https://jwc.htu.edu.cn/new/student/xsxk/xklx/01/kxkc"

# 选课接口（add / xk）
ADD_URL = "https://jwc.htu.edu.cn/new/student/xsxk/xklx/01/add"

# =========================
# 3. 请求头（Cookie 必须换成你的）
# =========================

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://jwc.htu.edu.cn",
    "Referer": "https://jwc.htu.edu.cn/",
    "Cookie": "JSESSIONID=452DF0F434C557E9690CC83E27213CAF"
}

# =========================
# 4. 获取课程列表 payload（示例）
# =========================

KXKC_PAYLOAD = {
    "kcmc": "",
    "kclbdm": "",
    "xqdm": "1",
    "xkxqdm": "1",
    "xkfsdm": "1"
}


# =========================
# 5. 核心函数
# =========================

def fetch_courses():
    """获取课程列表（自动重试）"""
    for i in range(10):
        try:
            print(f"正在获取课程列表（第 {i+1} 次）...")
            r = requests.post(
                KXKC_URL,
                headers=HEADERS,
                data=KXKC_PAYLOAD,
                timeout=TIMEOUT,
                proxies=PROXIES
            )
            r.raise_for_status()
            data = r.json()
            rows = data.get("rows", [])
            if rows:
                return rows
        except Exception as e:
            print("获取失败，重试中：", e)
            time.sleep(2)
    return []


def show_courses(rows):
    print("\n===== 可选课程列表 =====\n")
    for idx, c in enumerate(rows):
        print(
            f"[{idx}] {c.get('kcmc')} | "
            f"分类:{c.get('kcflmc', '未知分类')} | "
            f"学分:{c.get('xf', '?')} | "
            f"教师:{c.get('teaxm')} | "
            f"时间:{c.get('sksj', '').strip()} | "
            f"人数:{c.get('jxbrs')}/{c.get('pkrs')}"
        )
    print()




def choose_course(rows):
    """人工选择课程"""
    while True:
        try:
            idx = int(input("请输入要选的课程编号（如 0）："))
            return rows[idx]
        except:
            print("输入错误，请重新输入")


def submit_course(course):
    """提交选课"""
    payload = {
        "kcrwdm": course["kcrwdm"],
        "kcmc": course["kcmc"],
        "qz": "-1",
        "hlct": "0"
    }

    r = requests.post(
        ADD_URL,
        headers=HEADERS,
        data=payload,
        timeout=TIMEOUT,
        proxies=PROXIES
    )
    return r.json()


# =========================
# 6. 主流程
# =========================

def main():
    rows = fetch_courses()
    if not rows:
        print("课程列表获取失败，退出")
        sys.exit(1)

    show_courses(rows)

    course = choose_course(rows)
    print(f"\n你选择了：{course['kcmc']}")

    print("正在提交选课请求...\n")
    result = submit_course(course)

    print("服务器返回：")
    print(result)


if __name__ == "__main__":
    main()
