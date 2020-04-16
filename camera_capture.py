import cv2
import os
import datetime
#参考
#カメラからの映像をリアルタイムで表示し、
#キーボードを押下したタイミングのフレームを静止画の画像ファイルとして切り出して保存するサンプルコード。
# https://note.nkmk.me/python-opencv-camera-to-still-image/
def save_frame_camera_cycle(device_num, dir_path, basename, cycle, ext='jpg', delay=1, window_name='frame'):
    cap = cv2.VideoCapture(device_num)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    n = 0
    while True:
        ret, frame = cap.read()
        cv2.imshow(window_name, frame)
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break
        if n == cycle:
            n = 0
            cv2.imwrite('{}_{}.{}'.format(base_path, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'), ext), frame)
        n += 1

    cv2.destroyWindow(window_name)

#OpenCVによって表示されるフレームをカウントしているためカメラのFPS設定ではなく表示される映像のFPSが基準となる。
# 30FPS程度で表示されるのであればcycle=300とすると10秒おきに画像が保存される。
#保存するフレームの周期を指定する変数cycleを小さい値にすると大量の画像が保存されてしまうので注意。
# 今の環境では約8 fpsだったので１０秒おきに保存する場合は80
save_frame_camera_cycle(1, 'data/temp', 'camera_capture_cycle', 80)
