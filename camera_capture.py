import cv2
import os
#カメラからの映像をリアルタイムで表示し、
#キーボードを押下したタイミングのフレームを静止画の画像ファイルとして切り出して保存するサンプルコード。
# https://note.nkmk.me/python-opencv-camera-to-still-image/
def save_frame_camera_key(device_num, dir_path, basename, ext='jpg', delay=1, window_name='frame'):
    cap = cv2.VideoCapture(device_num)#引数でカメラを選べる 0:PC内蔵カメラ, 1:USB Webカメラ

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)#ディレクトリの作成
    base_path = os.path.join(dir_path, basename)#パスを結合

    n = 0
    while True:
        ret, frame = cap.read()
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(delay) & 0xFF
        if key == ord('c'):#キーボードのcを押すと指定したディレクトリに<basename>_<連番>.<拡張子>というファイル名で静止画が保存される。
            cv2.imwrite('{}_{}.{}'.format(base_path, n, ext), frame)#番号を末尾につける
            n += 1
        elif key == ord('q'):#キーボードのqを押すと終了
            break

    cv2.destroyWindow(window_name)


save_frame_camera_key(1, 'data/temp', 'camera_capture')