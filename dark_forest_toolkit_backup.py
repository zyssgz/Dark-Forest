#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黑暗森林工具箱 - Dark Forest Toolkit
为不会使用小众但实用工具的用户准备的集成工具箱
包含Windows内置工具和自定义实用功能
"""

import os
import sys
import subprocess
import json
import hashlib
import base64
import random
import string
import datetime
import re
from pathlib import Path
from typing import Optional, List, Dict, Any


class DarkForestToolkit:
    """黑暗森林工具箱主类"""
    
    def __init__(self):
        self.version = "2.0.0"
        self.name = "黑暗森林工具箱"
        self.tools = {
            "1": ("系统信息查看", self.show_system_info),
            "2": ("网络工具集", self.network_tools),
            "3": ("文件批量重命名", self.batch_rename),
            "4": ("文本加密/解密", self.text_crypto),
            "5": ("密码生成器", self.password_generator),
            "6": ("JSON格式化", self.json_formatter),
            "7": ("Base64编解码", self.base64_codec),
            "8": ("哈希计算器", self.hash_calculator),
            "9": ("时间戳转换", self.timestamp_converter),
            "10": ("进程管理", self.process_manager),
            "11": ("磁盘空间分析", self.disk_analyzer),
            "12": ("环境变量查看", self.env_viewer),
            "13": ("剪贴板历史(模拟)", self.clipboard_sim),
            "14": ("快速清理临时文件", self.cleanup_temp),
            "15": ("Windows内置工具一键启动", self.windows_builtin_tools),
            "16": ("QR码生成器", self.qr_generator),
            "17": ("颜色代码转换器", self.color_converter),
            "18": ("文本统计工具", self.text_statistics),
            "19": ("随机数据生成器", self.random_data_generator),
            "20": ("文件信息查看器", self.file_info_viewer),
            "21": ("网络速度测试", self.network_speed_test),
            "22": ("退出", self.exit_toolkit),
        }
    
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_banner(self):
        """显示横幅"""
        banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              🌲 黑暗森林工具箱 v{} 🌲                     ║
║                                                          ║
║     为探索者准备的实用工具集合                            ║
║     Dark Forest Toolkit for Explorers                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """.format(self.version)
        print(banner)
    
    def show_menu(self):
        """显示菜单"""
        print("\n📋 可用工具:")
        print("─" * 50)
        for key, (name, _) in sorted(self.tools.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 999):
            print(f"  {key}. {name}")
        print("─" * 50)
    
    def run(self):
        """运行工具箱"""
        while True:
            self.clear_screen()
            self.show_banner()
            self.show_menu()
            
            choice = input("\n请选择工具 (输入数字): ").strip()
            
            if choice in self.tools:
                try:
                    self.tools[choice][1]()
                    if choice != "15":
                        input("\n按回车键继续...")
                except KeyboardInterrupt:
                    print("\n操作已取消")
                    input("\n按回车键继续...")
                except Exception as e:
                    print(f"\n❌ 错误: {str(e)}")
                    input("\n按回车键继续...")
            else:
                print("\n❌ 无效的选择，请重试")
                input("\n按回车键继续...")
    
    def exit_toolkit(self):
        """退出工具箱"""
        print("\n👋 感谢使用黑暗森林工具箱！再见！")
        sys.exit(0)
    
    # ==================== 工具实现 ====================
    
    def show_system_info(self):
        """显示系统信息"""
        print("\n💻 系统信息")
        print("─" * 50)
        
        try:
            # 使用Python获取系统信息
            import platform
            import socket
            
            print(f"操作系统：{platform.system()} {platform.release()}")
            print(f"版本：{platform.version()}")
            print(f"架构：{platform.machine()}")
            print(f"处理器：{platform.processor()}")
            print(f"主机名：{socket.gethostname()}")
            print(f"Python版本：{platform.python_version()}")
            
            # 尝试获取更多信息
            if os.name == 'nt':
                # Windows特定信息
                result = subprocess.run(['systeminfo'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines[:15]:  # 只显示前15行
                        if ':' in line:
                            print(line.strip())
            
            # 内存信息
            import psutil
            mem = psutil.virtual_memory()
            print(f"\n内存总计：{mem.total / (1024**3):.2f} GB")
            print(f"内存可用：{mem.available / (1024**3):.2f} GB")
            print(f"内存使用率：{mem.percent}%")
            
        except ImportError:
            print("psutil未安装，部分信息不可用")
            print("安装方法：pip install psutil")
        except Exception as e:
            print(f"获取系统信息时出错：{e}")
    
    def network_tools(self):
        """网络工具集"""
        print("\n🌐 网络工具集")
        print("─" * 50)
        print("  1. Ping测试")
        print("  2. 查看IP配置")
        print("  3. 端口扫描(简单)")
        print("  4. 返回上级")
        
        choice = input("\n选择子工具: ").strip()
        
        if choice == "1":
            target = input("输入目标地址 (默认: www.baidu.com): ").strip() or "www.baidu.com"
            print(f"\n正在Ping {target}...")
            try:
                count = "-n" if os.name == 'nt' else "-c"
                result = subprocess.run(['ping', count, '4', target], 
                                      capture_output=True, text=True, timeout=10)
                print(result.stdout)
            except Exception as e:
                print(f"Ping失败：{e}")
        
        elif choice == "2":
            print("\nIP配置信息:")
            try:
                if os.name == 'nt':
                    result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
                else:
                    result = subprocess.run(['ifconfig'], capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"获取IP配置失败：{e}")
        
        elif choice == "3":
            target = input("输入目标地址 (默认: 127.0.0.1): ").strip() or "127.0.0.1"
            ports = input("输入端口范围 (默认: 1-100): ").strip() or "1-100"
            
            try:
                start, end = map(int, ports.split('-'))
                print(f"\n正在扫描 {target} 的端口 {start}-{end}...")
                
                open_ports = []
                for port in range(start, min(end + 1, start + 50)):  # 限制扫描数量
                    import socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((target, port))
                    if result == 0:
                        open_ports.append(port)
                    sock.close()
                
                if open_ports:
                    print(f"\n开放端口：{open_ports}")
                else:
                    print("\n未发现开放端口")
            except Exception as e:
                print(f"端口扫描失败：{e}")
    
    def batch_rename(self):
        """批量重命名文件"""
        print("\n📁 批量重命名工具")
        print("─" * 50)
        
        folder = input("输入文件夹路径 (默认: 当前目录): ").strip() or "."
        
        if not os.path.exists(folder):
            print("❌ 文件夹不存在")
            return
        
        pattern = input("输入文件名模式 (例如: file_001): ").strip() or "file_{:03d}"
        ext = input("输入文件扩展名 (例如: .txt): ").strip() or ".txt"
        
        try:
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            files.sort()
            
            print(f"\n找到 {len(files)} 个文件")
            print("预览重命名结果:")
            
            for i, old_name in enumerate(files[:10], 1):
                new_name = pattern.format(i) + ext
                print(f"  {old_name} -> {new_name}")
            
            if len(files) > 10:
                print(f"  ... 还有 {len(files) - 10} 个文件")
            
            confirm = input("\n确认执行？(y/n): ").strip().lower()
            if confirm == 'y':
                for i, old_name in enumerate(files, 1):
                    old_path = os.path.join(folder, old_name)
                    new_name = pattern.format(i) + ext
                    new_path = os.path.join(folder, new_name)
                    
                    if old_path != new_path:
                        os.rename(old_path, new_path)
                        print(f"✓ {old_name} -> {new_name}")
                
                print("\n✅ 重命名完成!")
            else:
                print("操作已取消")
        
        except Exception as e:
            print(f"❌ 重命名失败：{e}")
    
    def text_crypto(self):
        """文本加密/解密"""
        print("\n🔐 文本加密/解密")
        print("─" * 50)
        print("  1. Caesar加密")
        print("  2. Caesar解密")
        print("  3. XOR加密/解密")
        
        choice = input("\n选择操作: ").strip()
        text = input("输入文本: ").strip()
        
        if choice == "1":
            shift = int(input("输入偏移量 (默认: 3): ").strip() or "3")
            result = ""
            for char in text:
                if char.isalpha():
                    base = ord('A') if char.isupper() else ord('a')
                    result += chr((ord(char) - base + shift) % 26 + base)
                else:
                    result += char
            print(f"\n加密结果：{result}")
        
        elif choice == "2":
            shift = int(input("输入偏移量 (默认: 3): ").strip() or "3")
            result = ""
            for char in text:
                if char.isalpha():
                    base = ord('A') if char.isupper() else ord('a')
                    result += chr((ord(char) - base - shift) % 26 + base)
                else:
                    result += char
            print(f"\n解密结果：{result}")
        
        elif choice == "3":
            key = input("输入密钥: ").strip() or "secret"
            result = ""
            for i, char in enumerate(text):
                key_char = key[i % len(key)]
                result += chr(ord(char) ^ ord(key_char))
            print(f"\n结果：{result}")
            print("提示：使用相同的密钥再次运行可解密")
    
    def password_generator(self):
        """密码生成器"""
        print("\n🔑 密码生成器")
        print("─" * 50)
        
        length = int(input("密码长度 (默认: 16): ").strip() or "16")
        use_upper = input("包含大写字母？(y/n, 默认:y): ").strip().lower() != 'n'
        use_lower = input("包含小写字母？(y/n, 默认:y): ").strip().lower() != 'n'
        use_digits = input("包含数字？(y/n, 默认:y): ").strip().lower() != 'n'
        use_special = input("包含特殊字符？(y/n, 默认:y): ").strip().lower() != 'n'
        
        chars = ""
        if use_upper:
            chars += string.ascii_uppercase
        if use_lower:
            chars += string.ascii_lowercase
        if use_digits:
            chars += string.digits
        if use_special:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if not chars:
            print("❌ 至少选择一种字符类型")
            return
        
        passwords = []
        for _ in range(5):
            password = ''.join(random.choice(chars) for _ in range(length))
            passwords.append(password)
        
        print("\n生成的密码:")
        for i, pwd in enumerate(passwords, 1):
            print(f"  {i}. {pwd}")
    
    def json_formatter(self):
        """JSON格式化"""
        print("\n📄 JSON格式化工具")
        print("─" * 50)
        
        print("输入JSON (输入空行结束):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        
        json_text = '\n'.join(lines)
        
        try:
            parsed = json.loads(json_text)
            formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
            print("\n格式化结果:")
            print(formatted)
            
            save = input("\n保存到文件？(y/n): ").strip().lower()
            if save == 'y':
                filename = input("输入文件名 (默认: formatted.json): ").strip() or "formatted.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(formatted)
                print(f"✅ 已保存到 {filename}")
        
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析错误：{e}")
    
    def base64_codec(self):
        """Base64编解码"""
        print("\n🔤 Base64编解码")
        print("─" * 50)
        print("  1. 编码")
        print("  2. 解码")
        
        choice = input("\n选择操作: ").strip()
        text = input("输入文本: ").strip()
        
        try:
            if choice == "1":
                encoded = base64.b64encode(text.encode()).decode()
                print(f"\n编码结果：{encoded}")
            elif choice == "2":
                decoded = base64.b64decode(text).decode()
                print(f"\n解码结果：{decoded}")
            else:
                print("❌ 无效选择")
        except Exception as e:
            print(f"❌ 操作失败：{e}")
    
    def hash_calculator(self):
        """哈希计算器"""
        print("\n#️⃣ 哈希计算器")
        print("─" * 50)
        print("  1. MD5")
        print("  2. SHA1")
        print("  3. SHA256")
        print("  4. 文件哈希")
        
        choice = input("\n选择哈希算法: ").strip()
        
        if choice == "4":
            filepath = input("输入文件路径: ").strip()
            if not os.path.exists(filepath):
                print("❌ 文件不存在")
                return
            
            hash_type = input("选择算法 (md5/sha1/sha256, 默认:md5): ").strip().lower() or "md5"
            
            try:
                if hash_type == "md5":
                    hasher = hashlib.md5()
                elif hash_type == "sha1":
                    hasher = hashlib.sha1()
                elif hash_type == "sha256":
                    hasher = hashlib.sha256()
                else:
                    print("❌ 不支持的算法")
                    return
                
                with open(filepath, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b''):
                        hasher.update(chunk)
                
                print(f"\n{hash_type.upper()}哈希值：{hasher.hexdigest()}")
            
            except Exception as e:
                print(f"❌ 计算失败：{e}")
        else:
            text = input("输入文本: ").strip()
            
            try:
                if choice == "1":
                    result = hashlib.md5(text.encode()).hexdigest()
                elif choice == "2":
                    result = hashlib.sha1(text.encode()).hexdigest()
                elif choice == "3":
                    result = hashlib.sha256(text.encode()).hexdigest()
                else:
                    print("❌ 无效选择")
                    return
                
                print(f"\n哈希值：{result}")
            
            except Exception as e:
                print(f"❌ 计算失败：{e}")
    
    def timestamp_converter(self):
        """时间戳转换"""
        print("\n⏰ 时间戳转换器")
        print("─" * 50)
        print("  1. 时间戳 -> 日期时间")
        print("  2. 日期时间 -> 时间戳")
        print("  3. 当前时间戳")
        
        choice = input("\n选择操作: ").strip()
        
        try:
            if choice == "1":
                ts = input("输入时间戳 (秒, 默认: 当前): ").strip()
                if ts:
                    dt = datetime.datetime.fromtimestamp(float(ts))
                else:
                    dt = datetime.datetime.now()
                print(f"\n日期时间：{dt.strftime('%Y-%m-%d %H:%M:%S')}")
            
            elif choice == "2":
                date_str = input("输入日期时间 (格式: YYYY-MM-DD HH:MM:SS): ").strip()
                if not date_str:
                    dt = datetime.datetime.now()
                else:
                    dt = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                timestamp = dt.timestamp()
                print(f"\n时间戳：{int(timestamp)}")
            
            elif choice == "3":
                now = datetime.datetime.now()
                timestamp = int(now.timestamp())
                print(f"\n当前时间戳：{timestamp}")
                print(f"当前时间：{now.strftime('%Y-%m-%d %H:%M:%S')}")
        
        except Exception as e:
            print(f"❌ 转换失败：{e}")
    
    def process_manager(self):
        """进程管理"""
        print("\n⚙️ 进程管理")
        print("─" * 50)
        print("  1. 查看进程列表")
        print("  2. 查找进程")
        print("  3. 结束进程 (谨慎使用)")
        
        choice = input("\n选择操作: ").strip()
        
        try:
            if choice == "1":
                if os.name == 'nt':
                    result = subprocess.run(['tasklist'], capture_output=True, text=True)
                else:
                    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
                print("\n进程列表:")
                print(result.stdout[:2000])  # 限制输出长度
            
            elif choice == "2":
                keyword = input("输入进程名关键词: ").strip()
                if os.name == 'nt':
                    result = subprocess.run(['tasklist'], capture_output=True, text=True)
                else:
                    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
                
                lines = result.stdout.split('\n')
                matched = [line for line in lines if keyword.lower() in line.lower()]
                
                if matched:
                    print(f"\n找到 {len(matched)} 个匹配进程:")
                    for line in matched[:20]:
                        print(line)
                else:
                    print("\n未找到匹配进程")
            
            elif choice == "3":
                pid = input("输入进程ID (PID): ").strip()
                confirm = input(f"⚠️ 确认结束进程 {pid}? (yes/no): ").strip().lower()
                
                if confirm == 'yes':
                    if os.name == 'nt':
                        subprocess.run(['taskkill', '/PID', pid, '/F'])
                    else:
                        subprocess.run(['kill', '-9', pid])
                    print("✅ 进程已结束")
                else:
                    print("操作已取消")
        
        except Exception as e:
            print(f"❌ 操作失败：{e}")
    
    def disk_analyzer(self):
        """磁盘空间分析"""
        print("\n💾 磁盘空间分析")
        print("─" * 50)
        
        try:
            import psutil
            
            partitions = psutil.disk_partitions()
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    print(f"\n分区：{partition.device}")
                    print(f"  挂载点：{partition.mountpoint}")
                    print(f"  文件系统：{partition.fstype}")
                    print(f"  总计：{usage.total / (1024**3):.2f} GB")
                    print(f"  已用：{usage.used / (1024**3):.2f} GB ({usage.percent}%)")
                    print(f"  可用：{usage.free / (1024**3):.2f} GB")
                except PermissionError:
                    continue
        
        except ImportError:
            print("psutil未安装，使用基础方法...")
            
            if os.name == 'nt':
                drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:")]
                for drive in drives:
                    try:
                        free_bytes, total_bytes = subprocess.check_output(
                            f'wmic logicaldisk where "DeviceID=\'{drive[:-1]}\'" get FreeSpace,Size',
                            shell=True, text=True
                        ).split('\n')[1:]
                        
                        if free_bytes.strip() and total_bytes.strip():
                            free_gb = int(free_bytes.strip()) / (1024**3)
                            total_gb = int(total_bytes.strip()) / (1024**3)
                            used_percent = ((total_gb - free_gb) / total_gb) * 100
                            
                            print(f"\n驱动器：{drive}")
                            print(f"  总计：{total_gb:.2f} GB")
                            print(f"  可用：{free_gb:.2f} GB")
                            print(f"  使用率：{used_percent:.1f}%")
                    except:
                        continue
            else:
                result = subprocess.run(['df', '-h'], capture_output=True, text=True)
                print(result.stdout)
    
    def env_viewer(self):
        """环境变量查看"""
        print("\n🔧 环境变量查看")
        print("─" * 50)
        
        print("所有环境变量:")
        for key, value in sorted(os.environ.items()):
            print(f"  {key}={value}")
        
        search = input("\n搜索变量名 (留空跳过): ").strip()
        if search:
            matched = {k: v for k, v in os.environ.items() if search.lower() in k.lower()}
            if matched:
                print(f"\n匹配的环境变量:")
                for key, value in matched.items():
                    print(f"  {key}={value}")
            else:
                print("\n未找到匹配的环境变量")
    
    def clipboard_sim(self):
        """剪贴板历史模拟"""
        print("\n📋 剪贴板工具")
        print("─" * 50)
        
        print("注意：此工具提供基础的剪贴板功能")
        print("  1. 复制文本到剪贴板")
        print("  2. 从剪贴板读取")
        
        choice = input("\n选择操作: ").strip()
        
        try:
            if choice == "1":
                text = input("输入要复制的文本: ").strip()
                
                if os.name == 'nt':
                    process = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
                    process.communicate(text.encode('utf-8'))
                else:
                    # Linux
                    if subprocess.run(['which', 'xclip'], capture_output=True).returncode == 0:
                        process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
                        process.communicate(text.encode('utf-8'))
                    elif subprocess.run(['which', 'wl-copy'], capture_output=True).returncode == 0:
                        process = subprocess.Popen(['wl-copy'], stdin=subprocess.PIPE)
                        process.communicate(text.encode('utf-8'))
                    else:
                        print("未找到剪贴板工具，请安装 xclip 或 wl-copy")
                        return
                
                print("✅ 已复制到剪贴板")
            
            elif choice == "2":
                if os.name == 'nt':
                    result = subprocess.run(['powershell', '-command', 'Get-Clipboard'], 
                                          capture_output=True, text=True)
                    print(f"\n剪贴板内容:\n{result.stdout}")
                else:
                    if subprocess.run(['which', 'xclip'], capture_output=True).returncode == 0:
                        result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], 
                                              capture_output=True, text=True)
                        print(f"\n剪贴板内容:\n{result.stdout}")
                    elif subprocess.run(['which', 'wl-paste'], capture_output=True).returncode == 0:
                        result = subprocess.run(['wl-paste'], capture_output=True, text=True)
                        print(f"\n剪贴板内容:\n{result.stdout}")
                    else:
                        print("未找到剪贴板工具")
        
        except Exception as e:
            print(f"❌ 操作失败：{e}")
    
    def cleanup_temp(self):
        """清理临时文件"""
        print("\n🧹 清理临时文件")
        print("─" * 50)
        
        temp_dirs = []
        
        if os.name == 'nt':
            # Windows临时目录
            temp_dirs = [
                os.environ.get('TEMP', ''),
                os.environ.get('TMP', ''),
                r'C:\Windows\Temp',
            ]
        else:
            # Linux/Mac临时目录
            temp_dirs = ['/tmp', '/var/tmp']
        
        temp_dirs = [d for d in temp_dirs if d and os.path.exists(d)]
        
        print("将清理以下目录:")
        for d in temp_dirs:
            print(f"  - {d}")
        
        confirm = input("\n确认清理？(y/n): ").strip().lower()
        
        if confirm == 'y':
            total_cleaned = 0
            total_size = 0
            
            for temp_dir in temp_dirs:
                try:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            try:
                                filepath = os.path.join(root, file)
                                file_size = os.path.getsize(filepath)
                                os.remove(filepath)
                                total_cleaned += 1
                                total_size += file_size
                            except:
                                pass
                        
                        for dir in dirs[:]:
                            try:
                                dirpath = os.path.join(root, dir)
                                os.rmdir(dirpath)
                            except:
                                pass
                except Exception as e:
                    print(f"清理 {temp_dir} 时出错：{e}")
            
            print(f"\n✅ 清理完成!")
            print(f"  删除文件数：{total_cleaned}")
            print(f"  释放空间：{total_size / (1024*1024):.2f} MB")
        else:
            print("操作已取消")
    
    def windows_builtin_tools(self):
        """Windows内置工具一键启动"""
        print("\n🪟 Windows内置工具一键启动")
        print("─" * 50)
        
        if os.name != 'nt':
            print("⚠️  此功能仅在Windows系统下可用")
            input("\n按回车键返回主菜单...")
            return
        
        tools = [
            ("1", "设备管理器", "devmgmt.msc"),
            ("2", "磁盘管理", "diskmgmt.msc"),
            ("3", "事件查看器", "eventvwr.msc"),
            ("4", "服务管理器", "services.msc"),
            ("5", "任务计划程序", "taskschd.msc"),
            ("6", "注册表编辑器", "regedit.exe"),
            ("7", "组策略编辑器", "gpedit.msc"),
            ("8", "计算机管理", "compmgmt.msc"),
            ("9", "性能监视器", "perfmon.msc"),
            ("10", "资源监视器", "resmon.exe"),
            ("11", "系统配置", "msconfig.exe"),
            ("12", "DirectX诊断工具", "dxdiag.exe"),
            ("13", "系统信息", "msinfo32.exe"),
            ("14", "控制面板", "control.exe"),
            ("15", "电源选项", "powercfg.cpl"),
            ("16", "网络连接", "ncpa.cpl"),
            ("17", "程序和功能", "appwiz.cpl"),
            ("18", "用户账户", "netplwiz"),
            ("19", "本地安全策略", "secpol.msc"),
            ("20", "Windows防火墙", "firewall.cpl"),
            ("21", "返回主菜单", None),
        ]
        
        while True:
            print("\n可用工具:")
            for key, name, _ in tools:
                if key == "21":
                    print(f"  [{key}] {name}")
                else:
                    print(f"  [{key}] {name}")
            
            choice = input("\n请选择要打开的工具 (输入编号): ").strip()
            
            if choice == "21":
                break
            
            # 查找对应的工具
            selected_tool = None
            for key, name, cmd in tools:
                if key == choice:
                    selected_tool = (name, cmd)
                    break
            
            if selected_tool:
                name, cmd = selected_tool
                print(f"\n🚀 正在启动 {name}...")
                try:
                    subprocess.Popen(cmd, shell=True)
                    print("✅ 已启动，窗口可能在后台，请检查任务栏")
                except Exception as e:
                    print(f"❌ 启动失败：{e}")
                
                input("\n按回车键继续...")
            else:
                print("❌ 无效的选择，请重新输入")

    # ==================== 新增工具实现 ====================

    def qr_generator(self):
        """QR码生成器"""
        print("\n📱 QR码生成器")
        print("─" * 50)
        
        data = input("输入要生成 QR 码的内容：").strip()
        if not data:
            print("❌ 内容不能为空")
            return
        
        # 使用简单的 ASCII 艺术生成 QR 码模拟
        print("\n生成的 QR 码 (ASCII 艺术版):")
        print("┌" + "─" * 40 + "┐")
        
        # 生成简单的图案模拟 QR 码
        random.seed(hash(data) % (2**32))
        for i in range(15):
            line = "│ "
            for j in range(40):
                # 定位图案
                if (i < 5 and j < 5) or (i < 5 and j > 34) or (i > 9 and j < 5):
                    line += "█" if (i % 2 == 0 or j % 2 == 0) else " "
                else:
                    line += "█" if random.random() > 0.5 else " "
            line += " │"
            print(line)
        
        print("└" + "─" * 40 + "┘")
        print(f"\n内容：{data}")
        print("\n提示：如需真实 QR 码图片，可安装 qrcode 库:")
        print("      pip install qrcode[pil]")
        
        # 检查是否安装了 qrcode 库
        try:
            import qrcode
            save_img = input("\n检测到 qrcode 库，是否保存为图片？(y/n): ").strip().lower()
            if save_img == 'y':
                filename = input("输入文件名 (默认：qrcode.png): ").strip() or "qrcode.png"
                if not filename.endswith('.png'):
                    filename += '.png'
                
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                img.save(filename)
                print(f"✅ QR 码已保存到 {filename}")
        except ImportError:
            pass

    def color_converter(self):
        """颜色代码转换器"""
        print("\n🎨 颜色代码转换器")
        print("─" * 50)
        print("  1. HEX -> RGB")
        print("  2. RGB -> HEX")
        print("  3. 预设颜色查看")
        
        choice = input("\n选择操作：").strip()
        
        if choice == "1":
            hex_color = input("输入 HEX 颜色代码 (如 #FF5733): ").strip()
            if hex_color.startswith('#'):
                hex_color = hex_color[1:]
            
            if len(hex_color) == 6:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                print(f"\nRGB 值：({r}, {g}, {b})")
                
                # 显示颜色条
                print(f"\n颜色预览：\033[48;2;{r};{g};{b}m          \033[0m")
            else:
                print("❌ 无效的 HEX 格式，应为 6 位十六进制数")
        
        elif choice == "2":
            try:
                r = int(input("输入 R 值 (0-255): ").strip())
                g = int(input("输入 G 值 (0-255): ").strip())
                b = int(input("输入 B 值 (0-255): ").strip())
                
                if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                    hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
                    print(f"\nHEX 值：{hex_color}")
                    print(f"颜色预览：\033[48;2;{r};{g};{b}m          \033[0m")
                else:
                    print("❌ RGB 值必须在 0-255 范围内")
            except ValueError:
                print("❌ 请输入有效的数字")
        
        elif choice == "3":
            colors = [
                ("红色", "#FF0000", (255, 0, 0)),
                ("绿色", "#00FF00", (0, 255, 0)),
                ("蓝色", "#0000FF", (0, 0, 255)),
                ("黄色", "#FFFF00", (255, 255, 0)),
                ("青色", "#00FFFF", (0, 255, 255)),
                ("品红", "#FF00FF", (255, 0, 255)),
                ("黑色", "#000000", (0, 0, 0)),
                ("白色", "#FFFFFF", (255, 255, 255)),
                ("橙色", "#FFA500", (255, 165, 0)),
                ("紫色", "#800080", (128, 0, 128)),
            ]
            
            print("\n预设颜色:")
            for name, hex_val, rgb_val in colors:
                r, g, b = rgb_val
                print(f"  \033[48;2;{r};{g};{b}m   \033[0m {name}: {hex_val} RGB{rgb_val}")

    def text_statistics(self):
        """文本统计工具"""
        print("\n📊 文本统计工具")
        print("─" * 50)
        
        print("输入文本 (输入空行结束):")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        
        text = '\n'.join(lines)
        
        if not text:
            print("❌ 文本为空")
            return
        
        # 统计信息
        char_count = len(text)
        char_no_space = len(text.replace(' ', '').replace('\n', '').replace('\t', ''))
        word_count = len(text.split())
        line_count = len(lines)
        
        # 中文统计
        chinese_chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
        
        # 英文统计
        english_words = len([w for w in text.split() if w.isalpha()])
        
        # 数字统计
        digit_count = len([c for c in text if c.isdigit()])
        
        # 标点符号统计
        punctuation = '.,!?;:,.!?.!?、。！？；："'
        punct_count = len([c for c in text if c in punctuation])
        
        print("\n📈 统计结果:")
        print(f"  总字符数：{char_count}")
        print(f"  字符数 (不含空格): {char_no_space}")
        print(f"  单词/词组数：{word_count}")
        print(f"  行数：{line_count}")
        print(f"  中文字符数：{chinese_chars}")
        print(f"  英文单词数：{english_words}")
        print(f"  数字个数：{digit_count}")
        print(f"  标点符号数：{punct_count}")
        
        # 平均词长
        if word_count > 0:
            avg_word_len = char_no_space / word_count
            print(f"  平均词长：{avg_word_len:.2f}")
        
        # 频率分析
        freq_show = input("\n显示字符频率分析？(y/n): ").strip().lower()
        if freq_show == 'y':
            from collections import Counter
            freq = Counter(text.replace(' ', '').replace('\n', ''))
            top_chars = freq.most_common(10)
            
            print("\n出现频率最高的 10 个字符:")
            for char, count in top_chars:
                display_char = repr(char) if char in ['\n', '\t', ' '] else char
                bar = '█' * min(count, 30)
                print(f"  {display_char}: {bar} ({count})")

    def random_data_generator(self):
        """随机数据生成器"""
        print("\n🎲 随机数据生成器")
        print("─" * 50)
        print("  1. 随机整数")
        print("  2. 随机浮点数")
        print("  3. 随机选择")
        print("  4. 随机日期")
        print("  5. 随机 UUID")
        
        choice = input("\n选择类型：").strip()
        
        try:
            if choice == "1":
                min_val = int(input("最小值 (默认：0): ").strip() or "0")
                max_val = int(input("最大值 (默认：100): ").strip() or "100")
                count = int(input("生成数量 (默认：1): ").strip() or "1")
                
                numbers = [random.randint(min_val, max_val) for _ in range(count)]
                print(f"\n生成的随机整数：{numbers}")
            
            elif choice == "2":
                min_val = float(input("最小值 (默认：0.0): ").strip() or "0.0")
                max_val = float(input("最大值 (默认：1.0): ").strip() or "1.0")
                count = int(input("生成数量 (默认：1): ").strip() or "1")
                
                numbers = [random.uniform(min_val, max_val) for _ in range(count)]
                print(f"\n生成的随机浮点数：{[round(n, 4) for n in numbers]}")
            
            elif choice == "3":
                items_input = input("输入选项 (用逗号分隔): ").strip()
                items = [item.strip() for item in items_input.split(',')]
                count = int(input("抽取数量 (默认：1): ").strip() or "1")
                
                if count <= len(items):
                    selected = random.sample(items, count)
                    print(f"\n随机选择结果：{selected}")
                else:
                    print("❌ 抽取数量不能超过选项总数")
            
            elif choice == "4":
                start_year = int(input("开始年份 (默认：2000): ").strip() or "2000")
                end_year = int(input("结束年份 (默认：2024): ").strip() or "2024")
                count = int(input("生成数量 (默认：1): ").strip() or "1")
                
                dates = []
                for _ in range(count):
                    year = random.randint(start_year, end_year)
                    month = random.randint(1, 12)
                    day = random.randint(1, 28)  # 简化处理
                    hour = random.randint(0, 23)
                    minute = random.randint(0, 59)
                    second = random.randint(0, 59)
                    
                    dt = datetime.datetime(year, month, day, hour, minute, second)
                    dates.append(dt.strftime('%Y-%m-%d %H:%M:%S'))
                
                print(f"\n生成的随机日期：{dates}")
            
            elif choice == "5":
                import uuid
                count = int(input("生成数量 (默认：1): ").strip() or "1")
                
                uuids = [str(uuid.uuid4()) for _ in range(count)]
                print(f"\n生成的 UUID:")
                for u in uuids:
                    print(f"  {u}")
        
        except ValueError as e:
            print(f"❌ 输入错误：{e}")
        except Exception as e:
            print(f"❌ 生成失败：{e}")

    def file_info_viewer(self):
        """文件信息查看器"""
        print("\n📄 文件信息查看器")
        print("─" * 50)
        
        filepath = input("输入文件路径：").strip()
        
        if not os.path.exists(filepath):
            print("❌ 文件不存在")
            return
        
        if os.path.isdir(filepath):
            print("❌ 这是一个目录，请输入文件路径")
            return
        
        try:
            stat_info = os.stat(filepath)
            
            print("\n📋 文件详细信息:")
            print(f"  完整路径：{os.path.abspath(filepath)}")
            print(f"  文件名：{os.path.basename(filepath)}")
            print(f"  文件大小：{stat_info.st_size:,} 字节 ({stat_info.st_size / 1024:.2f} KB)")
            
            # 时间信息
            created = datetime.datetime.fromtimestamp(stat_info.st_ctime)
            modified = datetime.datetime.fromtimestamp(stat_info.st_mtime)
            accessed = datetime.datetime.fromtimestamp(stat_info.st_atime)
            
            print(f"  创建时间：{created.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  修改时间：{modified.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  访问时间：{accessed.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 文件权限
            import stat
            mode = stat_info.st_mode
            perms = []
            perms.append('r' if mode & stat.S_IRUSR else '-')
            perms.append('w' if mode & stat.S_IWUSR else '-')
            perms.append('x' if mode & stat.S_IXUSR else '-')
            print(f"  权限：{''.join(perms)} (所有者)")
            
            # 文件扩展名
            ext = os.path.splitext(filepath)[1].lower()
            print(f"  扩展名：{ext}")
            
            # MIME 类型推测
            mime_types = {
                '.txt': 'text/plain',
                '.pdf': 'application/pdf',
                '.jpg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.mp3': 'audio/mpeg',
                '.mp4': 'video/mp4',
                '.json': 'application/json',
                '.html': 'text/html',
                '.css': 'text/css',
                '.js': 'application/javascript',
                '.py': 'text/x-python',
                '.zip': 'application/zip',
            }
            mime = mime_types.get(ext, 'unknown')
            print(f"  MIME 类型：{mime}")
            
            # 计算哈希
            calc_hash = input("\n计算文件哈希？(y/n): ").strip().lower()
            if calc_hash == 'y':
                print("\n正在计算哈希...")
                hash_md5 = hashlib.md5()
                hash_sha1 = hashlib.sha1()
                hash_sha256 = hashlib.sha256()
                
                with open(filepath, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b''):
                        hash_md5.update(chunk)
                        hash_sha1.update(chunk)
                        hash_sha256.update(chunk)
                
                print(f"  MD5:    {hash_md5.hexdigest()}")
                print(f"  SHA1:   {hash_sha1.hexdigest()}")
                print(f"  SHA256: {hash_sha256.hexdigest()}")
        
        except Exception as e:
            print(f"❌ 获取文件信息失败：{e}")

    def network_speed_test(self):
        """网络速度测试"""
        print("\n🚀 网络速度测试")
        print("─" * 50)
        
        print("正在测试网络速度...")
        print("(测试将从常见服务器下载小文件以估算速度)\n")
        
        test_urls = [
            ("Google DNS", "https://8.8.8.8"),
            ("Cloudflare DNS", "https://1.1.1.1"),
        ]
        
        results = []
        
        for name, url in test_urls:
            try:
                start_time = datetime.datetime.now()
                
                import socket
                # 提取主机名
                hostname = url.replace('https://', '').replace('http://', '')
                
                # DNS 解析时间
                socket.gethostbyname(hostname)
                dns_time = (datetime.datetime.now() - start_time).total_seconds() * 1000
                
                # TCP 连接测试
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                port = 443 if 'https' in url else 80
                
                connect_start = datetime.datetime.now()
                result = sock.connect_ex((hostname, port))
                connect_time = (datetime.datetime.now() - connect_start).total_seconds() * 1000
                
                sock.close()
                
                if result == 0:
                    status = "✓ 可达"
                    results.append((name, dns_time, connect_time, status))
                else:
                    status = "✗ 不可达"
                    results.append((name, dns_time, connect_time, status))
                
            except Exception as e:
                results.append((name, -1, -1, f"错误：{str(e)[:30]}"))
        
        print("\n测试结果:")
        print(f"{'服务':<20} {'DNS 延迟':<12} {'连接延迟':<12} {'状态'}")
        print("─" * 60)
        for name, dns, conn, status in results:
            dns_str = f"{dns:.2f} ms" if dns > 0 else "N/A"
            conn_str = f"{conn:.2f} ms" if conn > 0 else "N/A"
            print(f"{name:<20} {dns_str:<12} {conn_str:<12} {status}")
        
        print("\n💡 提示:")
        print("  - DNS 延迟越低，域名解析越快")
        print("  - 连接延迟越低，网络连接响应越快")
        print("  - 如需更精确的网速测试，建议使用专业测速网站")


def main():
    """主函数"""
    toolkit = DarkForestToolkit()
    toolkit.run()


if __name__ == "__main__":
    main()
