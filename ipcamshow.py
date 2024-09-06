# this code works with the HikVision IP cameras.
# I'm not sure if other IP cameras will work properly.
import cv2
import threading
import numpy as np

global_frames = None
capture_locks = None

total_channels = 9
is_captured = [False] * total_channels

prev_cnt = 0
all_captured_cnt = 0
all_captured_event = threading.Event()


def capture_video(index, url):
    global all_captured_cnt

    # Capture video from an RTSP stream and store the frames in a global variable.
    cap = cv2.VideoCapture(url)
    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Failed to capture from {url}")
            break
        # Store the frame in the global variable with thread safety
        with capture_locks[index]:
            global_frames[index] = frame

            is_captured[index] = True
            if all(is_captured):
                all_captured_event.set()
                is_captured[:] = [False] * len(is_captured)
                all_captured_cnt = all_captured_cnt + 1


def start_calc_fps():
    global prev_cnt
    global all_captured_cnt

    print('====== capture fps : ', all_captured_cnt - prev_cnt)
    prev_cnt = all_captured_cnt

    timer = threading.Timer(1, start_calc_fps)
    timer.start()


def display_videos(frame_cnt):
    # Create a blank canvas
    rows = 3
    cols = len(cctv_urls) // rows
    
    height, width, _ = (360, 640, 3)
    canvas = np.zeros((rows * height, cols * width, 3), dtype=np.uint8)
        
    # Display the frames from all the CCTV streams in a single window.
    while True:
        if all_captured_event.is_set():
            # Place the frames on the canvas
            for i, frame in enumerate(global_frames):
                if frame is not None:
                    with capture_locks[i]:
                        resize_frame = cv2.resize(frame, (width, height))
                        y = (i // cols) * height
                        x = (i % cols) * width
                        canvas[y:y + height, x:x + width, :] = resize_frame

            cv2.imshow('CCTV Feeds', canvas)
            frame_cnt = frame_cnt + 1
            print('------ capture frame count # ', all_captured_cnt, 'display frame count # ', frame_cnt)
            all_captured_event.clear()
        else:
            all_captured_event.wait(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    # RTSP URLs for different CCTV cameras
    cctv_urls = [
        'rtsp://admin:aikl1004!@towerdev.aikl.co.kr:101/Streaming/Channels/101/',
        'rtsp://admin:aikl1004!@towerdev.aikl.co.kr:102/Streaming/Channels/101/',
        'rtsp://admin:aikl1004!@towerdev.aikl.co.kr:103/Streaming/Channels/101/',
        'rtsp://admin:aikl1004!@towerdev.aikl.co.kr:104/Streaming/Channels/101/',
        'rtsp://admin:aikl1004!@towerdev.aikl.co.kr:105/Streaming/Channels/101/',
        'rtsp://admin:aikl1004!@towerdev.aikl.co.kr:106/Streaming/Channels/101/',
        'rtsp://admin:aikl1004!@towerdev.aikl.co.kr:107/Streaming/Channels/101/',
        'rtsp://admin:aikl1004!@towerdev.aikl.co.kr:108/Streaming/Channels/101/',
        'rtsp://admin:aikl1004!@towerdev.aikl.co.kr:109/Streaming/Channels/101/'
    ]

    is_captured = [False] * total_channels

    global_frames = [None] * len(cctv_urls)
    capture_locks = [threading.Lock() for _ in cctv_urls]

    start_calc_fps()

    # Start threads to capture each CCTV stream
    threads = []
    for i, url in enumerate(cctv_urls):
        thread = threading.Thread(target=capture_video, args=(i, url))
        thread.daemon = True
        thread.start()
        threads.append(thread)

    # Display the videos in a single window
    display_videos(0)

    # Join threads
    for thread in threads:
        thread.join()