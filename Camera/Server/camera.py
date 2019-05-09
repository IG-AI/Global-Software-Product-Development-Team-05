import cv2
import socket

class VideoCamera(object):
    def __init__(self, ip, port):
        # Using OpenCV to capture from device 0: VideoCapture(0), example webcam.
        # For IP Camera (From device like smartphone, VideoCapture("IP address: port")
        self.checkIP(ip, int(port, 10))
        self.video = cv2.VideoCapture("http://" + ip + ":" + port + "/video")

    def __del__(self):
        if hasattr(self, 'video'):
            self.video.release()
            cv2.destroyAllWindows()

    def checkIP(self, ip, port):
        s = socket.socket()
        s.settimeout(3)
        try:
            s.connect((ip, port))
            s.close()
        except:
           raise AssertionError("WRONG IP")

    def get_frame(self):
            success, image = self.video.read()
            (w, h, c) = image.shape
            image = cv2.resize(image,(600, 400))

            # We are using Motion JPEG, but OpenCV defaults to capture raw images,
            # so we must encode it into JPEG in order to correctly display the
            # video stream.
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()