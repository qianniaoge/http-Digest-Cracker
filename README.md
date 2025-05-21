# HTTP Digest Cracker

**Digest认证口令批量猜测工具**

`http-Digest-Cracker` 是一个 Python 工具，用于对 HTTP Digest 认证进行批量口令猜测（爆破）。支持多线程、URL 存活检测、自定义 User-Agent、进度条显示，并忽略 SSL 错误。结果实时保存到本地文件，适用于安全测试场景。

⚠️ **注意**：本工具仅限用于合法授权的渗透测试或安全研究，未经许可的爆破行为违法。

## 功能特性

- **URL 存活检测**：在爆破前检查 URL，仅处理返回 401 状态码（需要 Digest 认证）的目标。
- **多线程支持**：通过命令行参数自定义线程数，加速爆破过程。
- **自定义 User-Agent**：使用指定的 User-Agent 头，模拟特定设备请求。
- **进度条**：通过 `tqdm` 显示实时爆破进度。
- **实时结果保存**：成功认证的凭据实时写入本地文件 `success_results.txt`。
- **忽略 SSL 错误**：适合测试弱证书或自签名证书的目标。
- **线程安全**：使用锁机制确保结果写入的线程安全。

## 安装

### 环境要求
- Python 3.6+
- 依赖库：`requests`, `urllib3`, `tqdm`

### 安装步骤
1. 克隆仓库：
   ```bash
   git clone https://github.com/your-username/http-Digest-Cracker.git
   cd http-Digest-Cracker
   安装依赖：
bash

pip install requests urllib3 tqdm

使用方法
输入文件准备
在项目根目录下创建以下文件：
url.txt：目标 URL 列表，每行一个，例如：

https://example.com
http://test.com/admin

user.txt：用户名列表，每行一个，例如：

admin
user
test

pass.txt：密码列表，每行一个，例如：

password123
admin
123456

运行程序
在项目根目录下运行 main.py：
bash

python main.py

自定义线程数（默认 10）：
bash

python main.py --threads 20

输出
终端输出：显示 URL 存活检测结果、爆破进度、成功凭据。

文件输出：成功凭据实时写入 success_results.txt，格式如下：

=== HTTP Digest认证爆破成功结果 ===
成功: https://example.com 用户名: admin 密码: password123

若无成功结果或无存活 URL，会记录相应信息。

示例输出
假设 url.txt 包含 3 个 URL，user.txt 包含 2 个用户名，pass.txt 包含 3 个密码：

=== 开始URL存活检测 ===
URL存活且需要Digest认证: https://example.com
URL http://test.com 返回状态码 200，跳过
URL http://invalid.com 无法访问: Connection refused

=== 开始爆破 ===
爆破进度: 100%|██████████| 6/6 [00:02<00:00, 2.50尝试/s]
成功: https://example.com 用户名: admin 密码: password123

=== 爆破结果 ===
成功: https://example.com 用户名: admin 密码: password123

success_results.txt 内容：

=== HTTP Digest认证爆破成功结果 ===
成功: https://example.com 用户名: admin 密码: password123

文件结构

http-Digest-Cracker/
├── main.py               # 主程序文件
├── url.txt               # 目标 URL 列表
├── user.txt              # 用户名列表
├── pass.txt              # 密码列表
├── success_results.txt    # 爆破成功结果（自动生成）
└── README.md             # 项目文档

配置说明
User-Agent：默认使用以下 UA，可在 main.py 中修改 USER_AGENT 变量：

Mozilla/5.0 (Linux; U; Android 2.2; fr-fr; Desire_A8181 Build/FRF91) App3leWebKit/53.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1

线程数：通过 --threads 参数设置，建议根据网络和目标服务器调整（10-50 较常见）。

超时：请求超时设为 5 秒，可在 main.py 中修改 timeout 参数。

结果文件：成功结果保存到 success_results.txt，每次运行会清空文件。

注意事项
合法性：仅用于授权的安全测试，未经许可的爆破行为违法。

性能：过高线程数可能导致网络拥堵或触发目标服务器防御，建议测试后调整。

结果文件：运行前会清空 success_results.txt，如需保留历史结果，请备份。

错误处理：程序处理了文件缺失、网络错误等情况，错误信息会打印到终端。

贡献
欢迎提交 issue 或 pull request！请确保代码符合 PEP 8 规范，并附上详细说明。
许可证
MIT License (LICENSE)
