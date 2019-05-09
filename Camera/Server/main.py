from flask import Flask, render_template, Response, request
from camera import VideoCamera
from flask_cors import CORS
from flask import jsonify
import cv2

app = Flask(__name__)
CORS(app)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    camera.video.release()
    cv2.destroyAllWindows()


@app.route('/video_feed')
def video_feed():
    id = request.args.get("id")
    ip, port = id.split(':')
    try:
        camera = VideoCamera(ip, port)
        response = Response(
            gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')
        return response
    except:
        img = cv2.imread('novideo.jpg')
        data = cv2.imencode('.jpg', img)[1].tobytes()
        return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'
                        + data
                        + b'\r\n\r\n',
                        mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
