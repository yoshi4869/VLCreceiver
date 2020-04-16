import cv2
import os
import datetime
import sys
camera_id = 1 # 0:PCカメラ, 1:USBカメラ


#参考
#カメラからの映像をリアルタイムで表示し、
#キーボードを押下したタイミングのフレームを静止画の画像ファイルとして切り出して保存するサンプルコード。
#OpenCVで再生（表示）されている動画のFPSを測定し、画像に描画して重畳表示する方法を追加
# https://note.nkmk.me/python-opencv-camera-to-still-image/
def save_frame_camera_cycle(device_num, dir_path, basename, cycle, ext='jpg', delay=1, window_name='frame'):
    cap = cv2.VideoCapture(device_num)
    cap.set(cv2.CAP_PROP_FPS, 30) #30 fps設定はできた

    if not cap.isOpened():
        sys.exit()
    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)
    tm = cv2.TickMeter()
    tm.start()
    count = 0
    max_count = 10
    fps = 0

    n = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if count == max_count:
            tm.stop()
            fps = max_count / tm.getTimeSec()#FPSはFrames Per Secondなので、「フレーム数」を「そのフレームを表示するのに掛かった時間（秒）」で割れば求められる
            tm.reset()
            tm.start()
            count = 0

        cv2.putText(frame, 'FPS: {:.2f}'.format(fps),
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), thickness=2)
        cv2.imshow(window_name, frame)
        count += 1
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
save_frame_camera_cycle(camera_id, 'data/temp', 'camera_capture_cycle', 300)
