import requests
from pathlib import Path
import os
import time
import logging
import shutil
import tempfile
import subprocess

def setup_logging(log_filename):
    # 设置日志配置
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # 添加控制台输出
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def download_hosts(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises an exception if the request failed.
    return response.text

def parse_hosts(hosts_text):
    """Parse the hosts text into a dictionary."""
    lines = hosts_text.splitlines()
    hosts_dict = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        if len(parts) >= 2:
            ip_address = parts[0]
            hostnames = parts[1:]
            hosts_dict[' '.join([h for h in hostnames])] = ip_address
    return hosts_dict

def update_hosts_file(new_hosts_dict, local_hosts_path):
    # 创建备份文件
    backup_path = local_hosts_path.with_name(local_hosts_path.name + ".bak")
    
    # 如果原始文件存在，则创建备份文件
    if local_hosts_path.exists():
        shutil.copy2(local_hosts_path, backup_path)

    # 尝试更新文件
    temp_hosts_path = Path(tempfile.gettempdir()) / "temp_hosts"
    
    # 读取已存在的 hosts 文件内容
    existing_hosts_dict = {}
    if local_hosts_path.exists():
        with open(local_hosts_path, 'r') as file:
            existing_hosts_text = file.read()
            existing_hosts_dict = parse_hosts(existing_hosts_text)

    # 更新现有的 hosts 字典
    updated_hosts_dict = {**existing_hosts_dict, **new_hosts_dict}

    # 将更新后的字典转换回文本格式
    new_hosts_text = ""
    for hostname, ip_address in updated_hosts_dict.items():
        new_hosts_text += f"{ip_address} {hostname}\n"

    # 写入新的内容到临时文件
    with open(temp_hosts_path, 'w') as file:
        file.write(new_hosts_text)

    # 验证新文件
    try:
        with open(temp_hosts_path, 'r') as file:
            temp_hosts_text = file.read()
            assert temp_hosts_text == new_hosts_text, "New hosts file does not match expected content."
    except AssertionError as e:
        logging.error(f"Failed to validate new hosts file: {e}")
        return
    
    # 替换原有文件
    try:
        os.replace(temp_hosts_path, local_hosts_path)
        logging.info("Hosts file updated successfully.")
    except Exception as e:
        logging.error(f"Failed to replace hosts file: {e}")
        # 如果替换失败，恢复备份文件
        if backup_path.exists():
            shutil.copy2(backup_path, local_hosts_path)
            logging.info("Recovered original hosts file.")

def main():
    log_filename = "hosts_updater.log"
    setup_logging(log_filename)

    url = "https://gitee.com/if-the-wind/github-hosts/raw/main/hosts"
    local_hosts_path = Path(r"C:\Windows\System32\drivers\etc\hosts")

    logging.info("Starting hosts updater...")

    while True:
        try:
            # 下载最新的 hosts 文件
            latest_hosts_text = download_hosts(url)
            
            # 解析新的 hosts 文件
            new_hosts_dict = parse_hosts(latest_hosts_text)
            
            # 更新本地 hosts 文件
            update_hosts_file(new_hosts_dict, local_hosts_path)
        
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        command = ["ipconfig", "/flushdns"]
        result = subprocess.run(command, capture_output=True, text=True)
        logging.info(f"Flushed DNS cache: {result.stdout}")

        # 暂停一小时 (3600 秒)
        time.sleep(3600)

if __name__ == "__main__":
    main()

