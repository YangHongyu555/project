# 创建项目目录结构和文件内容
import os
import numpy as np
import cv2

# 项目文件夹路径
project_dir = '/mnt/data/cv-color'
os.makedirs(project_dir, exist_ok=True)

# 创建 main.py
main_py_content = """
import cv2
import numpy as np
from utils import detect_color_blocks

def main():
    # 读取图像
    img = cv2.imread('example.jpg')

    # 识别蓝色和黄色色块
    output_img = detect_color_blocks(img)

    # 保存处理后的图像
    cv2.imwrite('output.jpg', output_img)

    # 显示结果
    cv2.imshow('Detected Colors', output_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
"""

# 创建 utils.py
utils_py_content = """
import cv2
import numpy as np

def detect_color_blocks(img):
    # 转换为HSV色彩空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 蓝色和黄色的HSV范围
    blue_lower = np.array([100, 150, 50])
    blue_upper = np.array([140, 255, 255])
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([30, 255, 255])

    # 创建掩膜
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)

    # 合并两个颜色的掩膜
    mask = cv2.bitwise_or(blue_mask, yellow_mask)

    # 找到轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 在图像上绘制矩形框
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # 排除过小的区域
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return img
"""

# 创建 setup.py
setup_py_content = """
from setuptools import setup, find_packages

setup(
    name='cv-color',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'numpy',
    ],
)
"""

# 创建 README.md
readme_md_content = """
# CV-Color - 识别魔方蓝色和黄色色块

## 项目介绍
本项目使用 OpenCV 实现了从图像中识别蓝色和黄色色块，并在这些色块上绘制矩形框的功能。适用于魔方图像等含有特定颜色块的场景。

## 依赖
- opencv-python
- numpy

## 使用方法
1. 将目标图像放置在项目目录下，并命名为 `example.jpg`。
2. 运行 `main.py` 文件，程序会自动读取图像、识别颜色，并保存为 `output.jpg`。

## 示例效果
图像处理结果：识别到蓝色和黄色的区域，并在其周围绘制了绿色矩形框。
"""

# 创建文件并写入内容
file_paths = {
    'main.py': main_py_content,
    'utils.py': utils_py_content,
    'setup.py': setup_py_content,
    'README.md': readme_md_content
}

# 保存文件
for file_name, content in file_paths.items():
    with open(os.path.join(project_dir, file_name), 'w') as f:
        f.write(content)

# 提供一个默认的图像占位
default_image_path = os.path.join(project_dir, 'example.jpg')

# 创建一个简单的白色背景占位图
white_image = np.ones((400, 400, 3), dtype=np.uint8) * 255
cv2.imwrite(default_image_path, white_image)

# 返回文件夹路径
project_dir