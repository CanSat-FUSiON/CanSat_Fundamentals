from matplotlib import image
import numpy as np
import cv2
from time import sleep
from PIL import Image
import matplotlib.pyplot as plt


def main(sampleimage):
    image = cv2.imread(sampleimage)

    image_output(red_masks_get(image), 'images/sample_red.jpg')
    image_output(gray_get(image), 'images/sample_gray.jpg')
    image_output(binary_get(image), 'images/sample_binary.jpg')
    center_output(image, 'images/sample_center.jpg', center_get(image))

    print('Size:', size_get(image))
    print('Occupancy:', occ_get(image)*100, '%')
    print('Center:', center_get(image))


def image_output(image_data, image_name):
    img_arrange = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)  # グラフにするために形式変換
    plt.imshow(img_arrange)
    plt.savefig(image_name)  # 画像を出力する

# 重心座標と抽出画像を出力する関数


def center_output(sampleimage, image_name, center):
    img_arrange = cv2.cvtColor(red_masks_get(
        sampleimage), cv2.COLOR_BGR2RGB)  # グラフにするために形式変換
    plt.imshow(img_arrange)  # 画像をグラフに貼り付け

    x, y = center[0], center[1]
    plt.plot(x, y, marker='.')  # 重心座標をグラフに張り付け

    plt.savefig(image_name)  # グラフを表示

# HSVで特定の色を抽出する関数


def hsvExtraction(image, hsvLower, hsvUpper):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # 画像をHSVに変換
    hsv_mask = cv2.inRange(hsv, hsvLower, hsvUpper)  # HSVからマスクを作成
    result = cv2.bitwise_and(image, image, mask=hsv_mask)  # 元画像とマスクを合成
    return result


# 抽出画像データを取得する関数
def red_masks_get(image):

    # HSVでの色抽出
    hsvLower_0 = np.array([0, 80, 100])    # 抽出する色の下限0(赤の抽出のため二つにわけて合成が必要)
    hsvLower_1 = np.array([170, 80, 100])  # 抽出する色の下限1(赤の抽出のため二つにわけて合成が必要)
    hsvUpper_0 = np.array([10, 255, 255])    # 抽出する色の上限0(赤の抽出のため二つにわけて合成が必要)
    hsvUpper_1 = np.array([179, 255, 255])   # 抽出する色の上限1(赤の抽出のため二つにわけて合成が必要)

    hsvResult_0 = hsvExtraction(image, hsvLower_0, hsvUpper_0)  # 画像0を作成
    hsvResult_1 = hsvExtraction(image, hsvLower_1, hsvUpper_1)  # 画像1を作成

    hsvResult = hsvResult_0 | hsvResult_1  # 画像を統合

    return hsvResult


# グレースケール画像データを取得する関数
def gray_get(image):
    img = red_masks_get(image)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # グレースケールで画像を読み込み
    return img_gray


# 二値画像データを取得する関数
def binary_get(image):
    ret, img_binary = cv2.threshold(
        gray_get(image), 10, 255, cv2.THRESH_BINARY)  # 2値画像に変換
    return img_binary


# 占有率を求める関数
def occ_get(image):
    pixel_number = np.size(binary_get(image))  # 全ピクセル数
    pixel_sum = np.sum(binary_get(image))  # 輝度の合計数
    white_pixel_number = pixel_sum/255  # 白のピクセルの数

    return white_pixel_number / pixel_number  # 占有率を計算


# 重心座標を求める関数
def center_get(image):
    mu = cv2.moments(binary_get(image), False)  # 重心関数作成

    if mu["m00"] != 0:
        x, y = int(mu["m10"]/mu["m00"]), int(mu["m01"]/mu["m00"])  # 重心座標の作成
        return [x, y]  # 重心座標を返り値に設定

    else:
        return [-20000, -20000]  # ありえない数字を返す


# 画像のサイズの取得
def size_get(image):
    # img = cv2.imread(sampleimage)
    height, width, channel = image.shape
    return [width, height]


        