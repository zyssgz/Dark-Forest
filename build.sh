#!/bin/bash

echo "=========================================="
echo "  黑暗森林工具箱 - 自动打包构建脚本"
echo "=========================================="
echo ""

# 1. 检查主程序是否存在
if [ ! -f "dark_forest_toolkit.py" ]; then
    echo "[错误] 找不到 dark_forest_toolkit.py，请确保当前目录正确。"
    exit 1
fi

# 2. 清理旧的构建文件
echo "[1/4] 正在清理旧的构建文件..."
rm -rf build dist *.spec
echo "      清理完成。"

# 3. 开始打包
echo "[2/4] 正在调用 PyInstaller 进行打包 (这可能需要几分钟)..."
echo "      参数说明：--onefile(单文件), --windowed(无黑框), --name(输出名)"
pyinstaller --onefile --name "DarkForestToolkit" --clean dark_forest_toolkit.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[错误] 打包失败！请检查上方报错信息或是否安装了 pyinstaller (pip install pyinstaller)。"
    exit 1
fi

# 4. 整理输出
echo "[3/4] 打包成功！正在整理文件..."
mkdir -p Release
mv dist/DarkForestToolkit Release/ 2>/dev/null
if [ -f "Release/DarkForestToolkit" ]; then
    echo "      可执行文件已移至：./Release/DarkForestToolkit"
else
    echo "      [警告] 未找到生成的可执行文件。"
fi

# 清理临时构建目录以保持整洁
echo "[4/4] 清理临时构建目录..."
rm -rf build dist *.spec

echo ""
echo "=========================================="
echo "  构建完成！"
echo "  最新版本位于：./Release/DarkForestToolkit"
echo "=========================================="
echo ""
