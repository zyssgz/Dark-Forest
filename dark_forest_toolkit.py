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
        self.version = "1.0.0"
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
            "15": ("退出", self.exit_toolkit),
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


def main():
    """主函数"""
    toolkit = DarkForestToolkit()
    toolkit.run()


if __name__ == "__main__":
    main()
