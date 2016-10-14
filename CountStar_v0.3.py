#! 圆斑/重叠圆斑计数工具

import os
import otsu
import pylab
import numpy as np
import mahotas as mh
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance


FileName = input("输入测试图片名称（默认为edu.tif）：") or "edu.tif"
CurrentDir = os.getcwd()
global new_img, r_criterion, g_criterion, b_criterion, gaussian


def rgb_filter(r, g, b, image):
    image_data = image.load()
    new_image = Image.new("RGB", (image.size[0], image.size[1]), (0, 0, 0))
    criterion = [r, g, b]
    luminance = [0, 0, 0]
    filtered_luminance = [0, 0, 0]
    for w in range(img.size[0]):
        for h in range(img.size[1]):
            luminance += image_data[w, h]
            if image_data[w, h][0] > criterion[0]:
                filtered_luminance[0] += image_data[w, h][0]
                new_image.putpixel((w, h), (image_data[w, h][0], 0, 0))
            if image_data[w, h][1] > criterion[1]:
                filtered_luminance[1] += image_data[w, h][0]
                new_image.putpixel((w, h), (0, image_data[w, h][1], 0))
            if image_data[w, h][2] > criterion[2]:
                filtered_luminance[2] += image_data[w, h][0]
                new_image.putpixel((w, h), (0, 0, image_data[w, h][2]))
    return new_image, luminance, filtered_luminance


def image_processing(image, gaussian_blur):
    new_image = Image.new("RGB", (image.size[0], image.size[1]), (0, 0, 0))
    contrast = ImageEnhance.Contrast(image)
    # 图片预处理，参数可调整
    new_image = contrast.enhance(5.0)
    new_image = new_image.filter(ImageFilter.GaussianBlur(3))
    # 大津二值化
    new_image = new_image.convert('L')
    new_image = otsu.otsu(new_image)
    new_image = new_image.filter(ImageFilter.SMOOTH)
    # new_image.show()
    new_image.save("TEMP.PNG", "PNG")
    # 开始调用mahotas方法
    mahotas_image = mh.imread("TEMP.PNG")
    mahotas_image = mh.gaussian_filter(mahotas_image, gaussian_blur)
    # pylab.imshow(mhimgf)
    # pylab.show()
    mahotas_image = mahotas_image.astype(np.uint8)
    T = mh.thresholding.otsu(mahotas_image)
    labeled, number_of_spots = mh.label(mahotas_image > T)
    seeds_image = mh.regmax(mahotas_image)
    # pylab.imshow(mh.overlay(mahotas_image, seeds_image))
    # pylab.show()
    seeds, number_of_separated_spots = mh.label(seeds_image)
    return number_of_spots, number_of_separated_spots

# 设置经验参数
# 1. 设置RGB参数，过滤颜色较暗的斑点
while True:
    r_criterion = input("输入R通道参数（默认为0）：") or 0
    g_criterion = input("输入G通道参数（默认为0）：") or 0
    b_criterion = input("输入B通道参数（默认为0）：") or 0
    r_criterion = int(r_criterion)
    g_criterion = int(g_criterion)
    b_criterion = int(b_criterion)

    img = Image.open(CurrentDir + "/Test/" + FileName)
    new_img, lumi, flumi = rgb_filter(r_criterion, g_criterion, b_criterion, img)
    print("原图总亮度：R: %i G: %i B: %i" % (lumi[0], lumi[1], lumi[2]))
    print("修正总亮度：R: %i G: %i B: %i" % (flumi[0], flumi[1], flumi[2]))
    print("*****************************************")
    img.show()
    new_img.show()

    switch = input("中意吗QwQ？(y/n) ")
    if switch == "y":
        break

# 2.设置gaussian参数，用来设定对重叠细胞的分辨能力，数值越大分辨能力越低；一般设置为5-15之间
while True:
    gaussian = input("输入Gaussian参数（默认为6）：") or 6
    gaussian = int(gaussian)
    real_num = input("输入手动计数结果（默认为0）：") or 0
    real_num = int(real_num)
    n_objects, n_nuclei = image_processing(new_img, gaussian)
    print("拆分前斑点数：", n_objects)
    print("拆分后斑点数：", n_nuclei)
    print("误差：", real_num - n_nuclei)

    switch = input("中意吗QwQ？(y/n) ")
    if switch == "y":
        break

# 测试用
# dist = mh.distance(mhimgf > T)
# dist = dist.max() - dist
# dist -= dist.min()
# dist = dist/float(dist.ptp()) * 255
# dist = dist.astype(np.uint8)
# pylab.imshow(dist)
# pylab.show()
# nuclei = mh.cwatershed(dist, seeds)
# pylab.imshow(nuclei)
# pylab.show()

print("***参数调试完毕，进入主程序***")
img_dir = input("输入文件存储目录（默认为Image）：") or "Image"
data = open("NUCLEI_DATA", "w")
print("注意，请及时备份NUCLEI_DATA文件，每次运行程序将覆盖之")
queue = os.listdir(CurrentDir + "/" + img_dir)
for item in queue:
    headers = item.strip(".tif").split("_")
    for header in headers:
        data.write(header + " ")
    img = Image.open(CurrentDir + "/" + img_dir + "/" + item)
    new_img, lumi, flumi = rgb_filter(r_criterion, g_criterion, b_criterion, img)
    n_objects, n_nuclei = image_processing(new_img, gaussian)
    data.write(str(n_objects) + " " + str(n_nuclei) + "\n")
