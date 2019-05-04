import cv2
import socket

class VideoCamera(object):
    def __init__(self, ip, port):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        print("\nINIT HERE\n")
        self.checkIP(ip, int(port, 10))
        self.video = cv2.VideoCapture("http://" + ip + ":" + port + "/video")
        print(self.video)

        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        print("\n DELETED HERE \n")

        if hasattr(self, 'video'):
            self.video.release()
            cv2.waitKey(500)
            cv2.destroyAllWindows()
            cv2.waitKey(500)

    def checkIP(self, ip, port):
        s = socket.socket()
        s.settimeout(3)
        try:
            print("BEFORE CONNECT")
            s.connect((ip, port))
            print("AFTER CONNECT")
            s.close()
            print("CLOSE SUCCESS")
        except:
           raise AssertionError("WRONG IP")

    def get_frame(self):
            success, image = self.video.read()
            (w, h, c) = image.shape
            image = cv2.resize(image,(600, 400))
            print("\n")
            print(success)
            print("\n")

            # We are using Motion JPEG, but OpenCV defaults to capture raw images,
            # so we must encode it into JPEG in order to correctly display the
            # video stream.
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()