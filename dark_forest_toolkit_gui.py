#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黑暗森林工具箱 - GUI 版本
Dark Forest Toolkit - GUI Version
为小白用户设计的图形化界面工具箱
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
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog, simpledialog
from pathlib import Path
from typing import Optional, List, Dict, Any
import platform


class ModernStyle:
    """现代化样式配置"""
    # 颜色方案
    PRIMARY_COLOR = "#4A90E2"      # 主蓝色
    SECONDARY_COLOR = "#50C878"    # 次要绿色
    ACCENT_COLOR = "#FF6B6B"       # 强调红色
    BG_COLOR = "#F5F6FA"           # 背景色
    CARD_BG = "#FFFFFF"            # 卡片背景
    TEXT_COLOR = "#2D3436"         # 文字颜色
    TEXT_LIGHT = "#636E72"         # 浅色文字
    BORDER_COLOR = "#DFE6E9"       # 边框颜色
    
    # 圆角设置
    CORNER_RADIUS = 15
    BUTTON_RADIUS = 10
    
    # 字体
    FONT_TITLE = ("Microsoft YaHei UI", 16, "bold")
    FONT_SUBTITLE = ("Microsoft YaHei UI", 12)
    FONT_BODY = ("Microsoft YaHei UI", 10)
    FONT_BUTTON = ("Microsoft YaHei UI", 11, "bold")


class RoundedButton(tk.Canvas):
    """圆角按钮组件"""
    
    def __init__(self, parent, text, command=None, width=200, height=50, 
                 bg=ModernStyle.PRIMARY_COLOR, fg="white", **kwargs):
        super().__init__(parent, highlightthickness=0, **kwargs)
        self.config(width=width, height=height)
        
        self.command = command
        self.bg_color = bg
        self.fg_color = fg
        self.text = text
        
        self.radius = ModernStyle.BUTTON_RADIUS
        
        # 绘制圆角矩形
        self.draw_rounded_rect(0, 0, width, height, self.radius, fill=bg)
        
        # 添加文字
        self.text_item = self.create_text(
            width // 2, height // 2, 
            text=text, 
            fill=fg, 
            font=ModernStyle.FONT_BUTTON,
            anchor="center"
        )
        
        # 绑定点击事件
        self.bind("<Button-1>", self.on_click)
        self.text_item_bind = self.tag_bind(self.text_item, "<Button-1>", self.on_click)
        
        # 悬停效果
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.tag_bind(self.text_item, "<Enter>", self.on_enter)
        self.tag_bind(self.text_item, "<Leave>", self.on_leave)
    
    def draw_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        """绘制圆角矩形"""
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1,
        ]
        return self.create_polygon(points, smooth=True, outline="", **kwargs)
    
    def on_click(self, event=None):
        if self.command:
            self.command()
    
    def on_enter(self, event=None):
        """鼠标悬停效果"""
        lighter = self.lighten_color(self.bg_color, 20)
        self.itemconfig(self.find_withtag("all")[0], fill=lighter)
    
    def on_leave(self, event=None):
        """鼠标离开效果"""
        self.itemconfig(self.find_withtag("all")[0], fill=self.bg_color)
    
    def lighten_color(self, color, amount):
        """调亮颜色"""
        try:
            color = color.lstrip('#')
            lv = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            r, g, b = [min(255, v + amount) for v in lv]
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color


class ToolCard(tk.Frame):
    """工具卡片组件"""
    
    def __init__(self, parent, icon, title, description, command, **kwargs):
        super().__init__(parent, bg=ModernStyle.CARD_BG, **kwargs)
        self.config(highlightthickness=2, highlightbackground=ModernStyle.BORDER_COLOR)
        
        self.command = command
        
        # 布局
        self.grid_columnconfigure(0, weight=1)
        
        # 图标
        self.icon_label = tk.Label(
            self, text=icon, font=("Segoe UI Emoji", 24),
            bg=ModernStyle.CARD_BG
        )
        self.icon_label.grid(row=0, column=0, pady=(15, 5), sticky="n")
        
        # 标题
        self.title_label = tk.Label(
            self, text=title, font=ModernStyle.FONT_SUBTITLE,
            bg=ModernStyle.CARD_BG, fg=ModernStyle.TEXT_COLOR
        )
        self.title_label.grid(row=1, column=0, pady=(0, 5))
        
        # 描述
        self.desc_label = tk.Label(
            self, text=description, font=ModernStyle.FONT_BODY,
            bg=ModernStyle.CARD_BG, fg=ModernStyle.TEXT_LIGHT,
            wraplength=180
        )
        self.desc_label.grid(row=2, column=0, padx=10, pady=(0, 15))
        
        # 绑定点击事件
        for widget in [self.icon_label, self.title_label, self.desc_label]:
            widget.bind("<Button-1>", lambda e: self.command())
        
        # 悬停效果
        self.bind_hover_effect()
    
    def bind_hover_effect(self):
        """绑定悬停效果"""
        widgets = [self, self.icon_label, self.title_label, self.desc_label]
        for widget in widgets:
            widget.bind("<Enter>", self.on_enter)
            widget.bind("<Leave>", self.on_leave)
    
    def on_enter(self, event=None):
        self.config(highlightbackground=ModernStyle.PRIMARY_COLOR)
    
    def on_leave(self, event=None):
        self.config(highlightbackground=ModernStyle.BORDER_COLOR)


class DarkForestToolkitGUI:
    """黑暗森林工具箱 GUI 主类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌲 黑暗森林工具箱 - Dark Forest Toolkit")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap(default='')
        except:
            pass
        
        # 应用样式
        self.apply_modern_style()
        
        # 工具定义
        self.tools = self.get_tools_list()
        
        # 创建界面
        self.create_ui()
        
        # 当前打开的工具窗口
        self.tool_window = None
    
    def apply_modern_style(self):
        """应用现代化样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置通用样式
        style.configure(".", 
                       background=ModernStyle.BG_COLOR,
                       foreground=ModernStyle.TEXT_COLOR,
                       font=ModernStyle.FONT_BODY)
        
        style.configure("TFrame", background=ModernStyle.BG_COLOR)
        style.configure("TLabel", background=ModernStyle.BG_COLOR)
        
        # 按钮样式
        style.configure("TButton",
                       font=ModernStyle.FONT_BUTTON,
                       padding=10)
    
    def get_tools_list(self):
        """获取工具列表"""
        return [
            {"id": 1, "icon": "💻", "title": "系统信息", "desc": "查看计算机基本信息", "func": self.show_system_info},
            {"id": 2, "icon": "🌐", "title": "网络工具", "desc": "IP 查询、Ping 测试等", "func": self.network_tools},
            {"id": 3, "icon": "📝", "title": "批量重命名", "desc": "文件批量重命名工具", "func": self.batch_rename},
            {"id": 4, "icon": "🔐", "title": "文本加密", "desc": "加密和解密文本内容", "func": self.text_crypto},
            {"id": 5, "icon": "🔑", "title": "密码生成", "desc": "生成高强度随机密码", "func": self.password_generator},
            {"id": 6, "icon": "📋", "title": "JSON 格式化", "desc": "美化和格式化 JSON", "func": self.json_formatter},
            {"id": 7, "icon": "🔄", "title": "Base64 编解码", "desc": "Base64 编码解码工具", "func": self.base64_codec},
            {"id": 8, "icon": "🔢", "title": "哈希计算", "desc": "计算文件/文本哈希值", "func": self.hash_calculator},
            {"id": 9, "icon": "⏰", "title": "时间戳转换", "desc": "时间戳与日期互转", "func": self.timestamp_converter},
            {"id": 10, "icon": "⚙️", "title": "进程管理", "desc": "查看和管理进程", "func": self.process_manager},
            {"id": 11, "icon": "💾", "title": "磁盘分析", "desc": "分析磁盘空间使用", "func": self.disk_analyzer},
            {"id": 12, "icon": "🔧", "title": "环境变量", "desc": "查看系统环境变量", "func": self.env_viewer},
            {"id": 13, "icon": "📌", "title": "剪贴板", "desc": "剪贴板内容查看", "func": self.clipboard_sim},
            {"id": 14, "icon": "🧹", "title": "清理临时文件", "desc": "清理系统临时文件", "func": self.cleanup_temp},
            {"id": 15, "icon": "🛠️", "title": "Windows 工具", "desc": "启动 Windows 内置工具", "func": self.windows_builtin_tools},
            {"id": 16, "icon": "📱", "title": "QR 码生成", "desc": "生成二维码图片", "func": self.qr_generator},
            {"id": 17, "icon": "🎨", "title": "颜色转换", "desc": "颜色代码格式转换", "func": self.color_converter},
            {"id": 18, "icon": "📊", "title": "文本统计", "desc": "统计字数、行数等", "func": self.text_statistics},
            {"id": 19, "icon": "🎲", "title": "随机数据", "desc": "生成各类随机数据", "func": self.random_data_generator},
            {"id": 20, "icon": "📄", "title": "文件信息", "desc": "查看文件详细信息", "func": self.file_info_viewer},
            {"id": 21, "icon": "🚀", "title": "网速测试", "desc": "测试网络速度", "func": self.network_speed_test},
            {"id": 22, "icon": "✅", "title": "待办事项", "desc": "管理待办任务清单", "func": self.todo_manager},
            {"id": 23, "icon": "📐", "title": "单位转换", "desc": "常用单位换算", "func": self.unit_converter},
            {"id": 24, "icon": "🔍", "title": "正则测试", "desc": "测试正则表达式", "func": self.regex_tester},
            {"id": 25, "icon": "✂️", "title": "文件分割合并", "desc": "分割和合并文件", "func": self.file_splitter_merger},
            {"id": 26, "icon": "📈", "title": "系统监控", "desc": "实时监控系统资源", "func": self.system_monitor},
        ]
    
    def create_ui(self):
        """创建用户界面"""
        # 主容器
        main_container = tk.Frame(self.root, bg=ModernStyle.BG_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 顶部标题栏
        self.create_header(main_container)
        
        # 工具网格区域
        self.create_tools_grid(main_container)
        
        # 底部状态栏
        self.create_footer(main_container)
    
    def create_header(self, parent):
        """创建头部"""
        header_frame = tk.Frame(parent, bg=ModernStyle.CARD_BG, height=100)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # 圆角装饰（使用 Canvas 模拟）
        canvas = tk.Canvas(header_frame, bg=ModernStyle.CARD_BG, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # 绘制顶部圆角条
        canvas.create_arc(0, 0, 40, 40, start=90, extent=90, 
                         outline=ModernStyle.PRIMARY_COLOR, width=3, style=tk.ARC)
        canvas.create_arc(canvas.winfo_reqwidth()-40, 0, canvas.winfo_reqwidth(), 40,
                         start=0, extent=90, outline=ModernStyle.PRIMARY_COLOR, width=3, style=tk.ARC)
        
        # 标题
        title_label = tk.Label(
            canvas,
            text="🌲 黑暗森林工具箱",
            font=("Microsoft YaHei UI", 24, "bold"),
            bg=ModernStyle.CARD_BG,
            fg=ModernStyle.PRIMARY_COLOR
        )
        title_label.place(relx=0.5, rely=0.3, anchor="center")
        
        # 副标题
        subtitle_label = tk.Label(
            canvas,
            text="Dark Forest Toolkit - 为探索者准备的实用工具集",
            font=("Microsoft YaHei UI", 11),
            bg=ModernStyle.CARD_BG,
            fg=ModernStyle.TEXT_LIGHT
        )
        subtitle_label.place(relx=0.5, rely=0.7, anchor="center")
    
    def create_tools_grid(self, parent):
        """创建工具网格"""
        # 滚动区域
        canvas = tk.Canvas(parent, bg=ModernStyle.BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        
        # 工具容器
        tools_frame = tk.Frame(canvas, bg=ModernStyle.BG_COLOR)
        
        # 配置滚动
        tools_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=tools_frame, anchor="nw")
        
        def configure_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", configure_canvas)
        
        # 绑定鼠标滚轮
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # 布局
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 创建工具卡片
        row = 0
        col = 0
        cards_per_row = 4
        
        for tool in self.tools:
            card = ToolCard(
                tools_frame,
                icon=tool["icon"],
                title=tool["title"],
                description=tool["desc"],
                command=tool["func"]
            )
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            col += 1
            if col >= cards_per_row:
                col = 0
                row += 1
        
        # 配置网格权重
        for i in range(cards_per_row):
            tools_frame.grid_columnconfigure(i, weight=1)
    
    def create_footer(self, parent):
        """创建底部状态栏"""
        footer = tk.Frame(parent, bg=ModernStyle.CARD_BG, height=40)
        footer.pack(fill=tk.X, pady=(10, 0))
        footer.pack_propagate(False)
        
        # 版本信息
        version_label = tk.Label(
            footer,
            text="v2.1.0 GUI | Made with ❤️ for explorers",
            font=("Microsoft YaHei UI", 9),
            bg=ModernStyle.CARD_BG,
            fg=ModernStyle.TEXT_LIGHT
        )
        version_label.pack(side="left", padx=20, pady=10)
        
        # 系统信息
        system_label = tk.Label(
            footer,
            text=f"{platform.system()} {platform.release()}",
            font=("Microsoft YaHei UI", 9),
            bg=ModernStyle.CARD_BG,
            fg=ModernStyle.TEXT_LIGHT
        )
        system_label.pack(side="right", padx=20, pady=10)
    
    def create_tool_window(self, title):
        """创建工具窗口"""
        if self.tool_window and tk.Toplevel.winfo_exists(self.tool_window):
            self.tool_window.destroy()
        
        self.tool_window = tk.Toplevel(self.root)
        self.tool_window.title(title)
        self.tool_window.geometry("800x600")
        self.tool_window.minsize(600, 400)
        
        # 设置模态
        self.tool_window.transient(self.root)
        self.tool_window.grab_set()
        
        return self.tool_window
    
    # ==================== 工具实现 ====================
    
    def show_system_info(self):
        """显示系统信息"""
        window = self.create_tool_window("系统信息")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 收集系统信息
        info = []
        info.append(f"操作系统：{platform.system()} {platform.release()}")
        info.append(f"处理器：{platform.processor()}")
        info.append(f"Python 版本：{platform.python_version()}")
        info.append(f"架构：{platform.architecture()[0]}")
        info.append(f"机器名：{platform.node()}")
        info.append(f"CPU 核心数：{os.cpu_count()}")
        
        # 内存信息
        try:
            import psutil
            mem = psutil.virtual_memory()
            info.append(f"总内存：{mem.total / (1024**3):.2f} GB")
            info.append(f"可用内存：{mem.available / (1024**3):.2f} GB")
            info.append(f"内存使用率：{mem.percent}%")
        except ImportError:
            info.append("内存信息：安装 psutil 库以查看详细信息")
        
        # 显示信息
        text = scrolledtext.ScrolledText(
            frame, font=("Consolas", 11),
            bg=ModernStyle.CARD_BG,
            fg=ModernStyle.TEXT_COLOR
        )
        text.pack(fill=tk.BOTH, expand=True, pady=10)
        text.insert("1.0", "\n".join(info))
        text.config(state="disabled")
        
        # 关闭按钮
        close_btn = tk.Button(
            frame, text="关闭", font=ModernStyle.FONT_BUTTON,
            bg=ModernStyle.PRIMARY_COLOR, fg="white",
            command=window.destroy,
            padx=30, pady=10
        )
        close_btn.pack(pady=10)
    
    def network_tools(self):
        """网络工具"""
        window = self.create_tool_window("网络工具")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 选项卡
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Ping 测试
        ping_frame = tk.Frame(notebook, bg=ModernStyle.BG_COLOR)
        notebook.add(ping_frame, text="Ping 测试")
        
        tk.Label(ping_frame, text="目标地址:", bg=ModernStyle.BG_COLOR).pack(anchor="w", pady=5)
        ping_entry = tk.Entry(ping_frame, font=ModernStyle.FONT_BODY, width=50)
        ping_entry.insert(0, "www.baidu.com")
        ping_entry.pack(fill=tk.X, pady=5)
        
        ping_result = scrolledtext.ScrolledText(ping_frame, height=15, font=("Consolas", 10))
        ping_result.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def run_ping():
            target = ping_entry.get()
            ping_result.delete("1.0", tk.END)
            ping_result.insert("1.0", f"Pinging {target}...\n\n")
            try:
                result = subprocess.run(
                    ["ping", "-n", "4" if os.name == "nt" else "-c", "4", target],
                    capture_output=True, text=True, timeout=10
                )
                ping_result.insert(tk.END, result.stdout)
                if result.stderr:
                    ping_result.insert(tk.END, result.stderr)
            except Exception as e:
                ping_result.insert(tk.END, f"错误：{str(e)}")
        
        tk.Button(ping_frame, text="开始 Ping", command=run_ping,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=20, pady=5).pack()
        
        # IP 查询
        ip_frame = tk.Frame(notebook, bg=ModernStyle.BG_COLOR)
        notebook.add(ip_frame, text="IP 查询")
        
        ip_result = scrolledtext.ScrolledText(ip_frame, height=20, font=("Consolas", 10))
        ip_result.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def get_ip():
            ip_result.delete("1.0", tk.END)
            try:
                import socket
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                ip_result.insert("1.0", f"主机名：{hostname}\n本地 IP: {local_ip}\n")
                
                # 尝试获取公网 IP
                ip_result.insert(tk.END, "\n正在查询公网 IP...\n")
                import urllib.request
                pub_ip = urllib.request.urlopen('https://api.ipify.org', timeout=5).read().decode()
                ip_result.insert(tk.END, f"公网 IP: {pub_ip}\n")
            except Exception as e:
                ip_result.insert(tk.END, f"错误：{str(e)}")
        
        tk.Button(ip_frame, text="查询 IP", command=get_ip,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=20, pady=5).pack()
        
        # 关闭按钮
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def batch_rename(self):
        """批量重命名"""
        window = self.create_tool_window("批量重命名")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="选择文件夹:", bg=ModernStyle.BG_COLOR).pack(anchor="w")
        
        folder_var = tk.StringVar()
        folder_entry = tk.Entry(frame, textvariable=folder_var, font=ModernStyle.FONT_BODY)
        folder_entry.pack(fill=tk.X, pady=5)
        
        def select_folder():
            folder = filedialog.askdirectory()
            if folder:
                folder_var.set(folder)
        
        tk.Button(frame, text="浏览...", command=select_folder).pack(anchor="w")
        
        tk.Label(frame, text="命名模式:", bg=ModernStyle.BG_COLOR).pack(anchor="w", pady=(15, 5))
        tk.Label(frame, text="使用 {name}, {num}, {ext} 作为占位符", 
                bg=ModernStyle.BG_COLOR, fg=ModernStyle.TEXT_LIGHT).pack(anchor="w")
        
        pattern_entry = tk.Entry(frame, font=ModernStyle.FONT_BODY, width=50)
        pattern_entry.insert(0, "{name}_{num}.{ext}")
        pattern_entry.pack(fill=tk.X, pady=5)
        
        result_text = scrolledtext.ScrolledText(frame, height=15, font=("Consolas", 10))
        result_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def preview_rename():
            folder = folder_var.get()
            pattern = pattern_entry.get()
            
            if not folder or not os.path.isdir(folder):
                messagebox.showerror("错误", "请选择有效的文件夹")
                return
            
            result_text.delete("1.0", tk.END)
            result_text.insert("1.0", "预览:\n\n")
            
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
            for i, filename in enumerate(files[:10], 1):
                name, ext = os.path.splitext(filename)
                new_name = pattern.replace("{name}", name).replace("{num}", str(i)).replace("{ext}", ext[1:])
                result_text.insert(tk.END, f"{filename} → {new_name}\n")
            
            if len(files) > 10:
                result_text.insert(tk.END, f"\n... 还有 {len(files) - 10} 个文件")
        
        def execute_rename():
            if messagebox.askyesno("确认", "确定要执行批量重命名吗？此操作不可逆！"):
                preview_rename()
                messagebox.showinfo("完成", "批量重命名完成！")
        
        btn_frame = tk.Frame(frame, bg=ModernStyle.BG_COLOR)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="预览", command=preview_rename,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=20, pady=5).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="执行重命名", command=execute_rename,
                 bg=ModernStyle.SECONDARY_COLOR, fg="white",
                 padx=20, pady=5).pack(side="left", padx=5)
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def password_generator(self):
        """密码生成器"""
        window = self.create_tool_window("密码生成器")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 长度
        tk.Label(frame, text="密码长度:", bg=ModernStyle.BG_COLOR).pack(anchor="w")
        length_scale = tk.Scale(frame, from_=8, to=64, orient=tk.HORIZONTAL, 
                               length=300, bg=ModernStyle.BG_COLOR)
        length_scale.set(16)
        length_scale.pack(anchor="w", pady=5)
        
        # 选项
        use_upper = tk.BooleanVar(value=True)
        use_lower = tk.BooleanVar(value=True)
        use_digits = tk.BooleanVar(value=True)
        use_special = tk.BooleanVar(value=True)
        
        options_frame = tk.Frame(frame, bg=ModernStyle.BG_COLOR)
        options_frame.pack(anchor="w", pady=10)
        
        tk.Checkbutton(options_frame, text="大写字母 (A-Z)", variable=use_upper,
                      bg=ModernStyle.BG_COLOR).grid(row=0, column=0, sticky="w")
        tk.Checkbutton(options_frame, text="小写字母 (a-z)", variable=use_lower,
                      bg=ModernStyle.BG_COLOR).grid(row=0, column=1, sticky="w")
        tk.Checkbutton(options_frame, text="数字 (0-9)", variable=use_digits,
                      bg=ModernStyle.BG_COLOR).grid(row=1, column=0, sticky="w")
        tk.Checkbutton(options_frame, text="特殊字符 (!@#$)", variable=use_special,
                      bg=ModernStyle.BG_COLOR).grid(row=1, column=1, sticky="w")
        
        # 结果显示
        result_var = tk.StringVar()
        result_entry = tk.Entry(frame, textvariable=result_var, font=("Consolas", 16),
                               bg=ModernStyle.CARD_BG, relief="flat")
        result_entry.pack(fill=tk.X, pady=20, ipady=10)
        
        def generate():
            length = length_scale.get()
            chars = ""
            if use_upper.get():
                chars += string.ascii_uppercase
            if use_lower.get():
                chars += string.ascii_lowercase
            if use_digits.get():
                chars += string.digits
            if use_special.get():
                chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            
            if not chars:
                messagebox.showwarning("警告", "请至少选择一个字符类型")
                return
            
            password = ''.join(random.choice(chars) for _ in range(length))
            result_var.set(password)
        
        tk.Button(frame, text="生成密码", command=generate,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=40, pady=10, font=ModernStyle.FONT_BUTTON).pack()
        
        # 复制按钮
        def copy_to_clipboard():
            password = result_var.get()
            if password:
                window.clipboard_clear()
                window.clipboard_append(password)
                messagebox.showinfo("成功", "密码已复制到剪贴板!")
        
        tk.Button(frame, text="复制到剪贴板", command=copy_to_clipboard,
                 bg=ModernStyle.SECONDARY_COLOR, fg="white",
                 padx=20, pady=5).pack(pady=10)
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def json_formatter(self):
        """JSON 格式化"""
        window = self.create_tool_window("JSON 格式化")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 输入
        tk.Label(frame, text="输入 JSON:", bg=ModernStyle.BG_COLOR).pack(anchor="w")
        input_text = scrolledtext.ScrolledText(frame, height=10, font=("Consolas", 11))
        input_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 输出
        tk.Label(frame, text="格式化结果:", bg=ModernStyle.BG_COLOR).pack(anchor="w", pady=(15, 5))
        output_text = scrolledtext.ScrolledText(frame, height=10, font=("Consolas", 11))
        output_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        def format_json():
            input_data = input_text.get("1.0", tk.END).strip()
            output_text.delete("1.0", tk.END)
            
            if not input_data:
                output_text.insert("1.0", "请输入 JSON 数据")
                return
            
            try:
                parsed = json.loads(input_data)
                formatted = json.dumps(parsed, indent=4, ensure_ascii=False)
                output_text.insert("1.0", formatted)
            except json.JSONDecodeError as e:
                output_text.insert("1.0", f"JSON 错误：{str(e)}")
        
        def minify_json():
            input_data = input_text.get("1.0", tk.END).strip()
            output_text.delete("1.0", tk.END)
            
            try:
                parsed = json.loads(input_data)
                minified = json.dumps(parsed, separators=(',', ':'), ensure_ascii=False)
                output_text.insert("1.0", minified)
            except json.JSONDecodeError as e:
                output_text.insert("1.0", f"JSON 错误：{str(e)}")
        
        btn_frame = tk.Frame(frame, bg=ModernStyle.BG_COLOR)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="格式化", command=format_json,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=20, pady=5).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="压缩", command=minify_json,
                 bg=ModernStyle.SECONDARY_COLOR, fg="white",
                 padx=20, pady=5).pack(side="left", padx=5)
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def base64_codec(self):
        """Base64 编解码"""
        window = self.create_tool_window("Base64 编解码")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 输入
        tk.Label(frame, text="输入文本:", bg=ModernStyle.BG_COLOR).pack(anchor="w")
        input_text = scrolledtext.ScrolledText(frame, height=8, font=("Consolas", 11))
        input_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 输出
        tk.Label(frame, text="结果:", bg=ModernStyle.BG_COLOR).pack(anchor="w", pady=(15, 5))
        output_text = scrolledtext.ScrolledText(frame, height=8, font=("Consolas", 11))
        output_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        def encode():
            input_data = input_text.get("1.0", tk.END).strip()
            output_text.delete("1.0", tk.END)
            try:
                encoded = base64.b64encode(input_data.encode()).decode()
                output_text.insert("1.0", encoded)
            except Exception as e:
                output_text.insert("1.0", f"错误：{str(e)}")
        
        def decode():
            input_data = input_text.get("1.0", tk.END).strip()
            output_text.delete("1.0", tk.END)
            try:
                decoded = base64.b64decode(input_data).decode()
                output_text.insert("1.0", decoded)
            except Exception as e:
                output_text.insert("1.0", f"错误：{str(e)}")
        
        btn_frame = tk.Frame(frame, bg=ModernStyle.BG_COLOR)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="编码", command=encode,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=20, pady=5).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="解码", command=decode,
                 bg=ModernStyle.SECONDARY_COLOR, fg="white",
                 padx=20, pady=5).pack(side="left", padx=5)
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def hash_calculator(self):
        """哈希计算器"""
        window = self.create_tool_window("哈希计算器")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 文本哈希
        text_frame = tk.Frame(notebook, bg=ModernStyle.BG_COLOR)
        notebook.add(text_frame, text="文本哈希")
        
        tk.Label(text_frame, text="输入文本:", bg=ModernStyle.BG_COLOR).pack(anchor="w")
        text_input = scrolledtext.ScrolledText(text_frame, height=8, font=("Consolas", 11))
        text_input.pack(fill=tk.BOTH, expand=True, pady=5)
        
        result_text = scrolledtext.ScrolledText(text_frame, height=10, font=("Consolas", 10))
        result_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def calc_text_hash():
            text = text_input.get("1.0", tk.END).strip()
            result_text.delete("1.0", tk.END)
            
            hashes = {
                "MD5": hashlib.md5,
                "SHA1": hashlib.sha1,
                "SHA256": hashlib.sha256,
                "SHA512": hashlib.sha512
            }
            
            for name, func in hashes.items():
                h = func(text.encode()).hexdigest()
                result_text.insert(tk.END, f"{name}: {h}\n")
        
        tk.Button(text_frame, text="计算哈希", command=calc_text_hash,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=20, pady=5).pack()
        
        # 文件哈希
        file_frame = tk.Frame(notebook, bg=ModernStyle.BG_COLOR)
        notebook.add(file_frame, text="文件哈希")
        
        file_var = tk.StringVar()
        file_entry = tk.Entry(file_frame, textvariable=file_var, font=ModernStyle.FONT_BODY)
        file_entry.pack(fill=tk.X, pady=10)
        
        def select_file():
            filename = filedialog.askopenfilename()
            if filename:
                file_var.set(filename)
        
        tk.Button(file_frame, text="选择文件", command=select_file).pack()
        
        file_result = scrolledtext.ScrolledText(file_frame, height=10, font=("Consolas", 10))
        file_result.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def calc_file_hash():
            filename = file_var.get()
            file_result.delete("1.0", tk.END)
            
            if not filename or not os.path.isfile(filename):
                file_result.insert("1.0", "请选择有效文件")
                return
            
            file_result.insert("1.0", "计算中...\n")
            window.update()
            
            try:
                hashes = {
                    "MD5": hashlib.md5,
                    "SHA1": hashlib.sha1,
                    "SHA256": hashlib.sha256
                }
                
                for name, func in hashes.items():
                    h = func()
                    with open(filename, "rb") as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            h.update(chunk)
                    file_result.insert(tk.END, f"{name}: {h.hexdigest()}\n")
            except Exception as e:
                file_result.insert(tk.END, f"错误：{str(e)}")
        
        tk.Button(file_frame, text="计算文件哈希", command=calc_file_hash,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=20, pady=5).pack()
        
        # 关闭按钮
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def timestamp_converter(self):
        """时间戳转换器"""
        window = self.create_tool_window("时间戳转换")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 时间戳转日期
        ts_frame = tk.LabelFrame(frame, text="时间戳 → 日期时间", bg=ModernStyle.BG_COLOR)
        ts_frame.pack(fill=tk.X, pady=10)
        
        ts_entry = tk.Entry(ts_frame, font=ModernStyle.FONT_BODY, width=30)
        ts_entry.insert(0, str(int(datetime.datetime.now().timestamp())))
        ts_entry.pack(side="left", padx=5)
        
        ts_result = tk.Label(ts_frame, text="", bg=ModernStyle.CARD_BG, padx=10)
        ts_result.pack(side="left", fill=tk.X, expand=True, padx=5)
        
        def ts_to_date():
            try:
                ts = int(ts_entry.get())
                dt = datetime.datetime.fromtimestamp(ts)
                ts_result.config(text=dt.strftime("%Y-%m-%d %H:%M:%S"))
            except Exception as e:
                ts_result.config(text=f"错误：{e}")
        
        tk.Button(ts_frame, text="转换", command=ts_to_date).pack(side="left", padx=5)
        
        # 日期转时间戳
        date_frame = tk.LabelFrame(frame, text="日期时间 → 时间戳", bg=ModernStyle.BG_COLOR)
        date_frame.pack(fill=tk.X, pady=10)
        
        date_entry = tk.Entry(date_frame, font=ModernStyle.FONT_BODY, width=30)
        date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        date_entry.pack(side="left", padx=5)
        
        date_result = tk.Label(date_frame, text="", bg=ModernStyle.CARD_BG, padx=10)
        date_result.pack(side="left", fill=tk.X, expand=True, padx=5)
        
        def date_to_ts():
            try:
                dt = datetime.datetime.strptime(date_entry.get(), "%Y-%m-%d %H:%M:%S")
                ts = int(dt.timestamp())
                date_result.config(text=str(ts))
            except Exception as e:
                date_result.config(text=f"错误：{e}")
        
        tk.Button(date_frame, text="转换", command=date_to_ts).pack(side="left", padx=5)
        
        # 当前时间
        now_frame = tk.Frame(frame, bg=ModernStyle.BG_COLOR)
        now_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(now_frame, text="当前时间戳:", bg=ModernStyle.BG_COLOR).pack(anchor="w")
        current_ts = tk.Label(now_frame, text=str(int(datetime.datetime.now().timestamp())),
                             font=("Consolas", 16), bg=ModernStyle.CARD_BG, padx=20, pady=10)
        current_ts.pack(fill=tk.X, pady=5)
        
        def update_ts():
            current_ts.config(text=str(int(datetime.datetime.now().timestamp())))
            window.after(1000, update_ts)
        
        update_ts()
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def text_crypto(self):
        """文本加密解密"""
        window = self.create_tool_window("文本加密/解密")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="密钥:", bg=ModernStyle.BG_COLOR).pack(anchor="w")
        key_entry = tk.Entry(frame, font=ModernStyle.FONT_BODY, width=50)
        key_entry.pack(fill=tk.X, pady=5)
        
        tk.Label(frame, text="文本:", bg=ModernStyle.BG_COLOR).pack(anchor="w", pady=(15, 5))
        text_input = scrolledtext.ScrolledText(frame, height=8, font=("Consolas", 11))
        text_input.pack(fill=tk.BOTH, expand=True, pady=5)
        
        tk.Label(frame, text="结果:", bg=ModernStyle.BG_COLOR).pack(anchor="w", pady=(15, 5))
        result_output = scrolledtext.ScrolledText(frame, height=8, font=("Consolas", 11))
        result_output.pack(fill=tk.BOTH, expand=True, pady=5)
        
        def simple_encrypt(text, key):
            """简单 XOR 加密"""
            result = []
            key_bytes = key.encode() if isinstance(key, str) else key
            for i, char in enumerate(text):
                result.append(chr(ord(char) ^ key_bytes[i % len(key_bytes)]))
            return base64.b64encode(''.join(result).encode()).decode()
        
        def simple_decrypt(text, key):
            """简单 XOR 解密"""
            try:
                decoded = base64.b64decode(text).decode()
                result = []
                key_bytes = key.encode() if isinstance(key, str) else key
                for i, char in enumerate(decoded):
                    result.append(chr(ord(char) ^ key_bytes[i % len(key_bytes)]))
                return ''.join(result)
            except:
                return "解密失败，请检查密钥和密文"
        
        def encrypt():
            text = text_input.get("1.0", tk.END).strip()
            key = key_entry.get()
            if not key:
                messagebox.showwarning("警告", "请输入密钥")
                return
            result_output.delete("1.0", tk.END)
            result_output.insert("1.0", simple_encrypt(text, key))
        
        def decrypt():
            text = text_input.get("1.0", tk.END).strip()
            key = key_entry.get()
            if not key:
                messagebox.showwarning("警告", "请输入密钥")
                return
            result_output.delete("1.0", tk.END)
            result_output.insert("1.0", simple_decrypt(text, key))
        
        btn_frame = tk.Frame(frame, bg=ModernStyle.BG_COLOR)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="加密", command=encrypt,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=20, pady=5).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="解密", command=decrypt,
                 bg=ModernStyle.SECONDARY_COLOR, fg="white",
                 padx=20, pady=5).pack(side="left", padx=5)
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def cleanup_temp(self):
        """清理临时文件"""
        window = self.create_tool_window("清理临时文件")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="将要清理的位置:", bg=ModernStyle.BG_COLOR,
                font=ModernStyle.FONT_SUBTITLE).pack(anchor="w", pady=10)
        
        temp_locations = [
            ("系统临时文件夹", os.environ.get('TEMP', '')),
            ("用户临时文件夹", os.environ.get('TMP', '')),
            ("Python 缓存", "__pycache__"),
        ]
        
        for name, path in temp_locations:
            chk_frame = tk.Frame(frame, bg=ModernStyle.BG_COLOR)
            chk_frame.pack(fill=tk.X, pady=5)
            
            var = tk.BooleanVar(value=True)
            tk.Checkbutton(chk_frame, text=name, variable=var,
                          bg=ModernStyle.BG_COLOR).pack(side="left")
            tk.Label(chk_frame, text=path, bg=ModernStyle.BG_COLOR,
                    fg=ModernStyle.TEXT_LIGHT).pack(side="left", padx=10)
        
        log_text = scrolledtext.ScrolledText(frame, height=10, font=("Consolas", 10))
        log_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def cleanup():
            log_text.delete("1.0", tk.END)
            log_text.insert("1.0", "开始清理...\n\n")
            
            try:
                # 清理临时目录
                temp_dir = os.environ.get('TEMP', '')
                if temp_dir and os.path.exists(temp_dir):
                    count = 0
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            try:
                                os.remove(os.path.join(root, file))
                                count += 1
                            except:
                                pass
                    log_text.insert(tk.END, f"系统临时文件：清理了约 {count} 个文件\n")
                
                # 清理__pycache__
                pycache_count = 0
                for root, dirs, files in os.walk('.'):
                    if '__pycache__' in root:
                        for file in files:
                            try:
                                os.remove(os.path.join(root, file))
                                pycache_count += 1
                            except:
                                pass
                log_text.insert(tk.END, f"Python 缓存：清理了约 {pycache_count} 个文件\n")
                
                log_text.insert(tk.END, "\n✅ 清理完成!\n")
                messagebox.showinfo("完成", "临时文件清理完成!")
            except Exception as e:
                log_text.insert(tk.END, f"\n❌ 错误：{str(e)}\n")
        
        tk.Button(frame, text="开始清理", command=cleanup,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=30, pady=10, font=ModernStyle.FONT_BUTTON).pack()
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def windows_builtin_tools(self):
        """Windows 内置工具"""
        window = self.create_tool_window("Windows 内置工具")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tools = [
            ("记事本", "notepad"),
            ("计算器", "calc"),
            ("画图", "mspaint"),
            ("任务管理器", "taskmgr"),
            ("注册表编辑器", "regedit"),
            ("命令提示符", "cmd"),
            ("PowerShell", "powershell"),
            ("设备管理器", "devmgmt.msc"),
            ("磁盘管理", "diskmgmt.msc"),
            ("服务管理器", "services.msc"),
            ("事件查看器", "eventvwr.msc"),
            ("系统配置", "msconfig"),
        ]
        
        for name, cmd in tools:
            btn = tk.Button(
                frame, text=f"📌 {name}", command=lambda c=cmd: self.launch_app(c),
                bg=ModernStyle.CARD_BG, fg=ModernStyle.TEXT_COLOR,
                font=ModernStyle.FONT_BODY, anchor="w", padx=20, pady=10
            )
            btn.pack(fill=tk.X, pady=3)
            btn.bind("<Enter>", lambda e: e.widget.config(bg=ModernStyle.PRIMARY_COLOR, fg="white"))
            btn.bind("<Leave>", lambda e: e.widget.config(bg=ModernStyle.CARD_BG, fg=ModernStyle.TEXT_COLOR))
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=20)
    
    def launch_app(self, cmd):
        """启动应用程序"""
        try:
            subprocess.Popen(cmd, shell=True)
        except Exception as e:
            messagebox.showerror("错误", f"无法启动：{str(e)}")
    
    def qr_generator(self):
        """QR 码生成器"""
        window = self.create_tool_window("QR 码生成器")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="输入内容:", bg=ModernStyle.BG_COLOR).pack(anchor="w")
        content_entry = tk.Entry(frame, font=ModernStyle.FONT_BODY, width=50)
        content_entry.pack(fill=tk.X, pady=5)
        
        qr_label = tk.Label(frame, text="[QR 码将显示在这里]", bg=ModernStyle.CARD_BG,
                           padx=50, pady=50, relief="ridge")
        qr_label.pack(pady=20)
        
        def generate_qr():
            content = content_entry.get()
            if not content:
                messagebox.showwarning("警告", "请输入内容")
                return
            
            try:
                import qrcode
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(content)
                qr.make(fit=True)
                
                img = qr.make_image(fill_color="black", back_color="white")
                img.save("temp_qr.png")
                
                # 显示提示
                qr_label.config(text="✅ QR 码已保存为 temp_qr.png")
                messagebox.showinfo("成功", "QR 码已保存到 temp_qr.png")
            except ImportError:
                messagebox.showinfo("提示", "请安装 qrcode 库：pip install qrcode[pil]")
            except Exception as e:
                messagebox.showerror("错误", str(e))
        
        tk.Button(frame, text="生成 QR 码", command=generate_qr,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=30, pady=10).pack()
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def color_converter(self):
        """颜色转换器"""
        window = self.create_tool_window("颜色代码转换器")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 颜色预览
        preview = tk.Canvas(frame, width=200, height=100, bg="#4A90E2", highlightthickness=0)
        preview.pack(pady=10)
        
        tk.Label(frame, text="HEX:", bg=ModernStyle.BG_COLOR).pack(anchor="w")
        hex_entry = tk.Entry(frame, font=("Consolas", 14), width=20)
        hex_entry.insert(0, "#4A90E2")
        hex_entry.pack(pady=5)
        
        tk.Label(frame, text="RGB:", bg=ModernStyle.BG_COLOR).pack(anchor="w", pady=(15, 5))
        rgb_entry = tk.Entry(frame, font=("Consolas", 14), width=20)
        rgb_entry.insert(0, "rgb(74, 144, 226)")
        rgb_entry.pack(pady=5)
        
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def rgb_to_hex(r, g, b):
            return '#{:02x}{:02x}{:02x}'.format(r, g, b)
        
        def update_from_hex():
            hex_val = hex_entry.get().strip()
            try:
                r, g, b = hex_to_rgb(hex_val)
                rgb_entry.delete(0, tk.END)
                rgb_entry.insert(0, f"rgb({r}, {g}, {b})")
                preview.config(bg=hex_val)
            except:
                pass
        
        def update_from_rgb():
            rgb_val = rgb_entry.get().strip()
            try:
                match = re.search(r'(\d+),\s*(\d+),\s*(\d+)', rgb_val)
                if match:
                    r, g, b = map(int, match.groups())
                    hex_val = rgb_to_hex(r, g, b)
                    hex_entry.delete(0, tk.END)
                    hex_entry.insert(0, hex_val)
                    preview.config(bg=hex_val)
            except:
                pass
        
        hex_entry.bind("<KeyRelease>", lambda e: update_from_hex())
        rgb_entry.bind("<KeyRelease>", lambda e: update_from_rgb())
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=20)
    
    def text_statistics(self):
        """文本统计"""
        window = self.create_tool_window("文本统计工具")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        text_input = scrolledtext.ScrolledText(frame, height=15, font=("Consolas", 11))
        text_input.pack(fill=tk.BOTH, expand=True, pady=10)
        
        stats_label = tk.Label(frame, text="", bg=ModernStyle.CARD_BG,
                              font=ModernStyle.FONT_BODY, justify="left", padx=20, pady=20)
        stats_label.pack(fill=tk.X, pady=10)
        
        def calculate_stats():
            text = text_input.get("1.0", tk.END)
            
            chars = len(text)
            chars_no_space = len(text.replace(" ", "").replace("\n", ""))
            words = len(text.split())
            lines = text.count('\n')
            
            stats = f"""
            📊 统计结果:
            
            总字符数：{chars}
            非空字符数：{chars_no_space}
            单词数：{words}
            行数：{lines}
            """
            stats_label.config(text=stats)
        
        tk.Button(frame, text="统计", command=calculate_stats,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=30, pady=10).pack()
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def todo_manager(self):
        """待办事项管理器"""
        window = self.create_tool_window("待办事项管理器")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 输入框
        entry_frame = tk.Frame(frame, bg=ModernStyle.BG_COLOR)
        entry_frame.pack(fill=tk.X, pady=10)
        
        task_entry = tk.Entry(entry_frame, font=ModernStyle.FONT_BODY, width=40)
        task_entry.pack(side="left", padx=5)
        
        todo_list = []
        
        def add_task():
            task = task_entry.get().strip()
            if task:
                todo_list.append({"task": task, "done": False})
                refresh_list()
                task_entry.delete(0, tk.END)
        
        tk.Button(entry_frame, text="添加", command=add_task,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white").pack(side="left", padx=5)
        
        # 列表
        list_frame = tk.Frame(frame, bg=ModernStyle.BG_COLOR)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def refresh_list():
            for widget in list_frame.winfo_children():
                widget.destroy()
            
            for i, item in enumerate(todo_list):
                item_frame = tk.Frame(list_frame, bg=ModernStyle.CARD_BG)
                item_frame.pack(fill=tk.X, pady=2)
                
                var = tk.BooleanVar(value=item["done"])
                
                def toggle(idx, v=var):
                    todo_list[idx]["done"] = v.get()
                    refresh_list()
                
                cb = tk.Checkbutton(item_frame, text=item["task"], variable=var,
                                   command=lambda idx=i: toggle(idx),
                                   bg=ModernStyle.CARD_BG,
                                   font=("Microsoft YaHei UI", 11 if not item["done"] else 11, "normal" if not item["done"] else "overstrike"))
                cb.pack(side="left", padx=10)
                
                def delete(idx):
                    todo_list.pop(idx)
                    refresh_list()
                
                del_btn = tk.Button(item_frame, text="×", command=lambda idx=i: delete(idx),
                                   bg=ModernStyle.ACCENT_COLOR, fg="white", width=3)
                del_btn.pack(side="right", padx=5)
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def unit_converter(self):
        """单位转换器"""
        window = self.create_tool_window("单位转换器")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 长度转换
        length_frame = tk.Frame(notebook, bg=ModernStyle.BG_COLOR)
        notebook.add(length_frame, text="长度")
        
        conversions = {
            "米": 1,
            "千米": 1000,
            "厘米": 0.01,
            "毫米": 0.001,
            "英寸": 0.0254,
            "英尺": 0.3048,
            "英里": 1609.34
        }
        
        def create_converter(parent, units):
            input_frame = tk.Frame(parent, bg=ModernStyle.BG_COLOR)
            input_frame.pack(pady=10)
            
            val_entry = tk.Entry(input_frame, font=ModernStyle.FONT_BODY, width=15)
            val_entry.insert(0, "1")
            val_entry.pack(side="left", padx=5)
            
            from_unit = ttk.Combobox(input_frame, values=list(units.keys()), state="readonly")
            from_unit.current(0)
            from_unit.pack(side="left", padx=5)
            
            tk.Label(input_frame, text="→", bg=ModernStyle.BG_COLOR).pack(side="left", padx=5)
            
            to_unit = ttk.Combobox(input_frame, values=list(units.keys()), state="readonly")
            to_unit.current(1)
            to_unit.pack(side="left", padx=5)
            
            result_label = tk.Label(parent, text="", font=("Consolas", 16),
                                   bg=ModernStyle.CARD_BG, padx=20, pady=20)
            result_label.pack(fill=tk.X, pady=20)
            
            def convert():
                try:
                    val = float(val_entry.get())
                    from_u = from_unit.get()
                    to_u = to_unit.get()
                    
                    meters = val * units[from_u]
                    result = meters / units[to_u]
                    
                    result_label.config(text=f"{result:.6f} {to_u}")
                except:
                    result_label.config(text="输入错误")
            
            tk.Button(parent, text="转换", command=convert,
                     bg=ModernStyle.PRIMARY_COLOR, fg="white",
                     padx=20, pady=5).pack()
        
        create_converter(length_frame, conversions)
        
        # 重量转换
        weight_frame = tk.Frame(notebook, bg=ModernStyle.BG_COLOR)
        notebook.add(weight_frame, text="重量")
        
        weight_units = {
            "千克": 1,
            "克": 0.001,
            "吨": 1000,
            "磅": 0.453592,
            "盎司": 0.0283495
        }
        
        create_converter(weight_frame, weight_units)
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def regex_tester(self):
        """正则表达式测试"""
        window = self.create_tool_window("正则表达式测试")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="正则表达式:", bg=ModernStyle.BG_COLOR).pack(anchor="w")
        pattern_entry = tk.Entry(frame, font=("Consolas", 12), width=50)
        pattern_entry.insert(0, r"\d+")
        pattern_entry.pack(fill=tk.X, pady=5)
        
        tk.Label(frame, text="测试文本:", bg=ModernStyle.BG_COLOR).pack(anchor="w", pady=(15, 5))
        text_input = scrolledtext.ScrolledText(frame, height=8, font=("Consolas", 11))
        text_input.insert("1.0", "abc123def456ghi789")
        text_input.pack(fill=tk.BOTH, expand=True, pady=5)
        
        result_text = scrolledtext.ScrolledText(frame, height=10, font=("Consolas", 11))
        result_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def test_regex():
            pattern = pattern_entry.get()
            text = text_input.get("1.0", tk.END).strip()
            
            result_text.delete("1.0", tk.END)
            
            try:
                matches = re.findall(pattern, text)
                result_text.insert("1.0", f"找到 {len(matches)} 个匹配:\n\n")
                for i, match in enumerate(matches, 1):
                    result_text.insert(tk.END, f"{i}. {match}\n")
            except re.error as e:
                result_text.insert("1.0", f"正则表达式错误：{str(e)}")
        
        tk.Button(frame, text="测试", command=test_regex,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=30, pady=10).pack()
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def random_data_generator(self):
        """随机数据生成器"""
        window = self.create_tool_window("随机数据生成器")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 随机数
        num_frame = tk.Frame(notebook, bg=ModernStyle.BG_COLOR)
        notebook.add(num_frame, text="随机数")
        
        tk.Label(num_frame, text="范围:", bg=ModernStyle.BG_COLOR).pack(anchor="w")
        range_frame = tk.Frame(num_frame, bg=ModernStyle.BG_COLOR)
        range_frame.pack(anchor="w", pady=5)
        
        min_entry = tk.Entry(range_frame, width=10, font=ModernStyle.FONT_BODY)
        min_entry.insert(0, "1")
        min_entry.pack(side="left", padx=5)
        
        tk.Label(range_frame, text="-", bg=ModernStyle.BG_COLOR).pack(side="left")
        
        max_entry = tk.Entry(range_frame, width=10, font=ModernStyle.FONT_BODY)
        max_entry.insert(0, "100")
        max_entry.pack(side="left", padx=5)
        
        count_entry = tk.Entry(num_frame, width=10, font=ModernStyle.FONT_BODY)
        count_entry.insert(0, "10")
        count_entry.pack(anchor="w", pady=5)
        tk.Label(num_frame, text="生成个数", bg=ModernStyle.BG_COLOR).pack(anchor="w")
        
        num_result = scrolledtext.ScrolledText(num_frame, height=10, font=("Consolas", 11))
        num_result.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def gen_numbers():
            try:
                min_val = int(min_entry.get())
                max_val = int(max_entry.get())
                count = int(count_entry.get())
                
                numbers = [random.randint(min_val, max_val) for _ in range(count)]
                num_result.delete("1.0", tk.END)
                num_result.insert("1.0", ", ".join(map(str, numbers)))
            except Exception as e:
                num_result.delete("1.0", tk.END)
                num_result.insert("1.0", f"错误：{e}")
        
        tk.Button(num_frame, text="生成", command=gen_numbers,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=20, pady=5).pack()
        
        # UUID
        uuid_frame = tk.Frame(notebook, bg=ModernStyle.BG_COLOR)
        notebook.add(uuid_frame, text="UUID")
        
        uuid_result = scrolledtext.ScrolledText(uuid_frame, height=10, font=("Consolas", 11))
        uuid_result.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def gen_uuid():
            import uuid
            uuid_result.delete("1.0", tk.END)
            uuid_result.insert("1.0", str(uuid.uuid4()))
        
        tk.Button(uuid_frame, text="生成 UUID", command=gen_uuid,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=20, pady=5).pack()
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def file_info_viewer(self):
        """文件信息查看器"""
        window = self.create_tool_window("文件信息查看器")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        file_var = tk.StringVar()
        file_entry = tk.Entry(frame, textvariable=file_var, font=ModernStyle.FONT_BODY)
        file_entry.pack(fill=tk.X, pady=5)
        
        def select_file():
            filename = filedialog.askopenfilename()
            if filename:
                file_var.set(filename)
                show_info(filename)
        
        tk.Button(frame, text="选择文件", command=select_file).pack(pady=10)
        
        info_text = scrolledtext.ScrolledText(frame, height=20, font=("Consolas", 10))
        info_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def show_info(filename):
            info_text.delete("1.0", tk.END)
            
            try:
                stat = os.stat(filename)
                info = f"""
文件名：{os.path.basename(filename)}
完整路径：{filename}
文件大小：{stat.st_size:,} 字节 ({stat.st_size / 1024:.2f} KB)
创建时间：{datetime.datetime.fromtimestamp(stat.st_ctime)}
修改时间：{datetime.datetime.fromtimestamp(stat.st_mtime)}
访问时间：{datetime.datetime.fromtimestamp(stat.st_atime)}
                """
                info_text.insert("1.0", info)
            except Exception as e:
                info_text.insert("1.0", f"错误：{e}")
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def network_speed_test(self):
        """网络速度测试"""
        window = self.create_tool_window("网络速度测试")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        info_label = tk.Label(frame, text="点击下方按钮开始测试下载速度",
                             bg=ModernStyle.BG_COLOR, font=ModernStyle.FONT_SUBTITLE)
        info_label.pack(pady=20)
        
        result_label = tk.Label(frame, text="", bg=ModernStyle.CARD_BG,
                               font=("Consolas", 16), padx=20, pady=30)
        result_label.pack(fill=tk.X, pady=20)
        
        def test_speed():
            result_label.config(text="测试中...")
            window.update()
            
            try:
                import urllib.request
                import time
                
                # 测试 URL (使用一个小文件)
                url = "https://speed.hetzner.de/100MB.bin"
                start_time = time.time()
                
                response = urllib.request.urlopen(url, timeout=30)
                data = response.read()
                elapsed = time.time() - start_time
                
                speed_bps = len(data) * 8 / elapsed
                speed_mbps = speed_bps / 1_000_000
                
                result_label.config(text=f"下载速度：{speed_mbps:.2f} Mbps")
            except Exception as e:
                result_label.config(text=f"测试失败：{str(e)}")
        
        tk.Button(frame, text="开始测试", command=test_speed,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=40, pady=15, font=ModernStyle.FONT_BUTTON).pack()
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=20)
    
    def disk_analyzer(self):
        """磁盘分析"""
        window = self.create_tool_window("磁盘空间分析")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        result_text = scrolledtext.ScrolledText(frame, height=20, font=("Consolas", 11))
        result_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def analyze():
            result_text.delete("1.0", tk.END)
            
            try:
                import shutil
                
                partitions = []
                if os.name == 'nt':
                    import string
                    drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
                else:
                    drives = ["/"]
                
                for drive in drives:
                    try:
                        total, used, free = shutil.disk_usage(drive)
                        result_text.insert(tk.END, f"""
{'='*50}
驱动器：{drive}
{'='*50}
总容量：{total / (1024**3):.2f} GB
已使用：{used / (1024**3):.2f} GB ({used/total*100:.1f}%)
可用：{free / (1024**3):.2f} GB
""")
                    except:
                        pass
            except Exception as e:
                result_text.insert("1.0", f"错误：{e}")
        
        tk.Button(frame, text="分析磁盘", command=analyze,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=30, pady=10).pack()
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def env_viewer(self):
        """环境变量查看"""
        window = self.create_tool_window("环境变量查看")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        search_entry = tk.Entry(frame, font=ModernStyle.FONT_BODY, width=40)
        search_entry.pack(pady=5)
        search_entry.insert(0, "搜索环境变量...")
        
        env_text = scrolledtext.ScrolledText(frame, height=20, font=("Consolas", 10))
        env_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def show_env():
            env_text.delete("1.0", tk.END)
            search = search_entry.get()
            
            for key, value in sorted(os.environ.items()):
                if search.lower() in key.lower() or search == "搜索环境变量...":
                    env_text.insert(tk.END, f"{key}={value}\n\n")
        
        show_env()
        search_entry.bind("<KeyRelease>", lambda e: show_env())
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def process_manager(self):
        """进程管理"""
        window = self.create_tool_window("进程管理")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        process_text = scrolledtext.ScrolledText(frame, height=20, font=("Consolas", 10))
        process_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def show_processes():
            process_text.delete("1.0", tk.END)
            
            try:
                if os.name == 'nt':
                    result = subprocess.run(["tasklist"], capture_output=True, text=True)
                    process_text.insert("1.0", result.stdout)
                else:
                    result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
                    process_text.insert("1.0", result.stdout)
            except Exception as e:
                process_text.insert("1.0", f"错误：{e}")
        
        tk.Button(frame, text="刷新进程列表", command=show_processes,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=20, pady=5).pack(pady=5)
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def clipboard_sim(self):
        """剪贴板"""
        window = self.create_tool_window("剪贴板")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        clipboard_text = scrolledtext.ScrolledText(frame, height=15, font=("Consolas", 11))
        clipboard_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def show_clipboard():
            clipboard_text.delete("1.0", tk.END)
            try:
                content = window.clipboard_get()
                clipboard_text.insert("1.0", content)
            except:
                clipboard_text.insert("1.0", "剪贴板为空或无法访问")
        
        tk.Button(frame, text="读取剪贴板", command=show_clipboard,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=20, pady=5).pack(pady=5)
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def system_monitor(self):
        """系统监控"""
        window = self.create_tool_window("系统资源监控")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        monitor_text = scrolledtext.ScrolledText(frame, height=15, font=("Consolas", 11))
        monitor_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def update_monitor():
            try:
                import psutil
                
                cpu_percent = psutil.cpu_percent(interval=1)
                mem = psutil.virtual_memory()
                
                info = f"""
CPU 使用率：{cpu_percent}%
内存使用率：{mem.percent}%
内存可用：{mem.available / (1024**2):.2f} MB
                """
                monitor_text.delete("1.0", tk.END)
                monitor_text.insert("1.0", info)
            except ImportError:
                monitor_text.delete("1.0", tk.END)
                monitor_text.insert("1.0", "请安装 psutil 库：pip install psutil")
            except Exception as e:
                monitor_text.delete("1.0", tk.END)
                monitor_text.insert("1.0", f"错误：{e}")
            
            window.after(2000, update_monitor)
        
        tk.Button(frame, text="立即刷新", command=update_monitor,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=20, pady=5).pack(pady=5)
        
        update_monitor()
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def file_splitter_merger(self):
        """文件分割与合并"""
        window = self.create_tool_window("文件分割与合并")
        
        frame = tk.Frame(window, bg=ModernStyle.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 分割
        split_frame = tk.Frame(notebook, bg=ModernStyle.BG_COLOR)
        notebook.add(split_frame, text="分割")
        
        file_var = tk.StringVar()
        file_entry = tk.Entry(split_frame, textvariable=file_var, font=ModernStyle.FONT_BODY, width=50)
        file_entry.pack(fill=tk.X, pady=10)
        
        def select_file():
            filename = filedialog.askopenfilename()
            if filename:
                file_var.set(filename)
        
        tk.Button(split_frame, text="选择文件", command=select_file).pack()
        
        size_entry = tk.Entry(split_frame, width=10, font=ModernStyle.FONT_BODY)
        size_entry.insert(0, "1")
        size_entry.pack(pady=10)
        
        size_unit = ttk.Combobox(split_frame, values=["MB", "KB", "GB"], state="readonly", width=5)
        size_unit.current(0)
        size_unit.pack()
        
        def split_file():
            filename = file_var.get()
            if not filename or not os.path.isfile(filename):
                messagebox.showerror("错误", "请选择有效文件")
                return
            
            try:
                size = float(size_entry.get())
                unit = size_unit.get()
                multiplier = {"KB": 1024, "MB": 1024**2, "GB": 1024**3}[unit]
                chunk_size = int(size * multiplier)
                
                with open(filename, 'rb') as f:
                    chunk_num = 0
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        
                        out_file = f"{filename}.part{chunk_num:03d}"
                        with open(out_file, 'wb') as out:
                            out.write(chunk)
                        chunk_num += 1
                
                messagebox.showinfo("完成", f"文件已分割成 {chunk_num} 个部分")
            except Exception as e:
                messagebox.showerror("错误", str(e))
        
        tk.Button(split_frame, text="开始分割", command=split_file,
                 bg=ModernStyle.PRIMARY_COLOR, fg="white",
                 padx=20, pady=10).pack(pady=10)
        
        # 合并
        merge_frame = tk.Frame(notebook, bg=ModernStyle.BG_COLOR)
        notebook.add(merge_frame, text="合并")
        
        merge_dir_var = tk.StringVar()
        merge_dir_entry = tk.Entry(merge_frame, textvariable=merge_dir_var, font=ModernStyle.FONT_BODY, width=50)
        merge_dir_entry.pack(fill=tk.X, pady=10)
        
        def select_merge_dir():
            directory = filedialog.askdirectory()
            if directory:
                merge_dir_var.set(directory)
        
        tk.Button(merge_frame, text="选择包含 part 文件的文件夹", command=select_merge_dir).pack()
        
        def merge_files():
            directory = merge_dir_var.get()
            if not directory or not os.path.isdir(directory):
                messagebox.showerror("错误", "请选择有效文件夹")
                return
            
            try:
                parts = sorted([f for f in os.listdir(directory) if '.part' in f])
                if not parts:
                    messagebox.showerror("错误", "未找到 part 文件")
                    return
                
                output = filedialog.asksaveasfilename(defaultextension=".merged")
                if not output:
                    return
                
                with open(output, 'wb') as out:
                    for part in parts:
                        with open(os.path.join(directory, part), 'rb') as f:
                            out.write(f.read())
                
                messagebox.showinfo("完成", f"文件已合并到 {output}")
            except Exception as e:
                messagebox.showerror("错误", str(e))
        
        tk.Button(merge_frame, text="开始合并", command=merge_files,
                 bg=ModernStyle.SECONDARY_COLOR, fg="white",
                 padx=20, pady=10).pack(pady=10)
        
        tk.Button(frame, text="关闭", command=window.destroy,
                 bg=ModernStyle.ACCENT_COLOR, fg="white",
                 padx=30, pady=10).pack(pady=10)
    
    def run(self):
        """运行 GUI"""
        self.root.mainloop()


def main():
    """主函数"""
    app = DarkForestToolkitGUI()
    app.run()


if __name__ == "__main__":
    main()
