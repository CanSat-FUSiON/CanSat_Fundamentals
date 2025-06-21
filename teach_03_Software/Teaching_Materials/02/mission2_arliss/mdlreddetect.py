from matplotlib import image
import numpy as np
import cv2
from time import sleep
from PIL import Image


# HSVで特定の色を抽出する関数
def hsvExtraction(image, hsvLower, hsvUpper):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # 画像をHSVに変換
    hsv_mask = cv2.inRange(hsv, hsvLower, hsvUpper)  # HSVからマスクを作成
    result = cv2.bitwise_and(image, image, mask=hsv_mask)  # 元画像とマスクを合成
    return result


# 抽出画像データを取得する関数
def red_masks_get(image):
    # image = cv2.imread(sampleimage) # ファイル読み込み

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


# 回転角を取得(center:重心座標, size:画像サイズ, f_mm:焦点距離[mm], diagonal_mm:撮像素子の対角線[mm])
def rot_get(center, size, f_mm, diagonal_mm):

    if center != [-20000, -20000]:
        width_mm = diagonal_mm * size[0] / \
            np.sqrt(size[0]*size[0] + size[1]*size[1])
        sita_rad = np.arctan(
            (width_mm * (size[0] / 2 - center[0]) / size[0]) / f_mm)  # 回転角θ[rad]を導出
        sita = 180*sita_rad/np.pi

        return sita

    else:
        return 404000
