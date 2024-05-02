import cv2
from typing import Tuple

class CameraHandler():
    @staticmethod
    def start_webcam():
        camera = cv2.VideoCapture(0)
        while True:
            ret, frame = camera.read()
            cv2.imshow('Frame', frame)
            if cv2.waitKey(20) == 'q':
                break
            continue
        camera.release()
        cv2.destroyAllWindows()

    @staticmethod
    def record_video(filename: str, duration: int, 
                     resolution: Tuple[int] = (640, 480), 
                     fps: float = 20) -> None:
        camera = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(filename, fourcc, fps, (resolution[0], resolution[1]))
        
        max_frame_count = fps * duration
        current_frame_count = 0

        while camera.isOpened():
            ret, frame = camera.read()
            out.write(frame)
            if max_frame_count <= current_frame_count:
                break

            if cv2.waitKey(20) == 'q':
                break
            
            current_frame_count += 1
        
        camera.release()
        out.release()
        cv2.destroyAllWindows()