import cv2
import sys

#OpenCVで再生（表示）されている動画のFPSを測定し、画像に描画して重畳表示する方法

camera_id = 1
delay = 1
window_name = 'frame'

cap = cv2.VideoCapture(camera_id)

if not cap.isOpened():
    sys.exit()

tm = cv2.TickMeter()
tm.start()

count = 0
max_count = 10
fps = 0

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

cv2.destroyWindow(window_name)