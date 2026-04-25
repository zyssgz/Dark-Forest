# Dark-Forest

这个工具箱整理了多种实用的功能，如果想新增功能请在评论区中提出

## 🌲 黑暗森林工具箱 (Dark Forest Toolkit)

### 简介
为不会使用小众但实用工具的用户准备的集成工具箱，包含Windows内置工具和自定义实用功能。

### 功能列表

#### 🔧 系统工具
1. **系统信息查看** - 查看操作系统、硬件配置等详细信息
2. **进程管理** - 查看、搜索和管理系统进程
3. **磁盘空间分析** - 分析各分区使用情况
4. **环境变量查看** - 查看所有环境变量并支持搜索
5. **快速清理临时文件** - 一键清理系统临时文件
6. **Windows内置工具一键启动** - 20+个Windows系统工具快速启动（设备管理器、注册表编辑器、服务管理等）

#### 🌐 网络工具
7. **网络工具集** - Ping测试、IP配置查看、端口扫描

#### 📁 文件工具
8. **文件批量重命名** - 按模式批量重命名文件

#### 🔐 加密与安全
9. **文本加密/解密** - Caesar密码、XOR加密
10. **密码生成器** - 生成高强度随机密码
11. **Base64编解码** - 快速进行Base64编码和解码
12. **哈希计算器** - 计算MD5、SHA1、SHA256等哈希值

#### 📄 数据处理
13. **JSON格式化** - 美化和格式化JSON数据
14. **时间戳转换** - 时间戳与日期时间互相转换

#### 📋 其他工具
15. **剪贴板工具** - 复制和读取剪贴板内容

### 使用方法

#### 方式一：直接运行（需要Python环境）
```bash
python dark_forest_toolkit.py
```

或者在Linux/Mac上：
```bash
./dark_forest_toolkit.py
```

#### 方式二：使用可执行文件（推荐新手）
**Windows用户：**
1. 双击运行 `build.bat` 脚本
2. 等待打包完成
3. 在 `Release` 文件夹中找到 `DarkForestToolkit.exe`
4. 双击即可运行，无需安装Python！

**Linux/Mac用户：**
```bash
# 安装依赖
pip install pyinstaller

# 打包
pyinstaller --onefile --name "DarkForestToolkit" dark_forest_toolkit.py

# 运行
./dist/DarkForestToolkit
```

#### 自动打包说明
每次修改代码后，只需运行对应的构建脚本即可自动生成单一可执行文件：
- **Windows**: 双击 `build.bat`
- **Linux/Mac**: 运行 `chmod +x build.sh && ./build.sh`

打包完成后，可执行文件将保存在 `Release` 文件夹中。

#### 依赖安装（可选）
部分功能需要 `psutil` 库以获取更详细的系统信息：
```bash
pip install psutil
```

### 特点
- ✅ 跨平台支持（Windows/Linux/Mac）
- ✅ 纯Python实现，无需额外依赖（基础功能）
- ✅ 交互式菜单，简单易用
- ✅ **自动打包**：修改代码后一键生成单一可执行文件
- ✅ 适合不熟悉命令行的用户
- ✅ 持续更新更多实用工具

### 项目结构
```
Dark-Forest/
├── dark_forest_toolkit.py    # 主程序源代码
├── build.bat                 # Windows自动打包脚本
├── build.sh                  # Linux/Mac自动打包脚本
├── Release/                  # 打包输出的可执行文件
│   └── DarkForestToolkit     # (Linux/Mac) 或 DarkForestToolkit.exe (Windows)
└── README.md                 # 使用说明
```

### 注意事项
- 部分功能（如结束进程、清理文件）需要谨慎使用
- Windows某些功能可能需要管理员权限
- 建议在虚拟机或测试环境中先试用

---
**版本**: v1.0.0  
**作者**: Dark Forest Team

### 更新日志

#### v1.1.0
- ✨ 新增：Windows内置工具一键启动功能（20+个系统工具）
  - 设备管理器、磁盘管理、事件查看器
  - 服务管理器、注册表编辑器、组策略编辑器
  - 系统配置、DirectX诊断工具、性能监视器
  - 网络连接、电源选项、Windows防火墙等
- 🔄 优化：主菜单结构调整，功能分类更清晰
