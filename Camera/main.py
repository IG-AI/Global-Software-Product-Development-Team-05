#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from flask import Flask, render_template, Response, request
from camera import VideoCamera
from flask_cors import CORS
from flask import jsonify
import cv2

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
    camera.video.release()
    cv2.waitKey(500)
    cv2.destroyAllWindows()
    cv2.waitKey(500)


@app.route('/video_feed')
def video_feed():
    id = request.args.get("id")
    ip, port = id.split(':')
    print("PRINT ID", ip, int(port, 10))
    try:
        print("CREATE OBJECT CAMERA")
        camera = VideoCamera(ip, port)
        print("CREATE SUCCESS")
        response = Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')
        return response
    except:
        print("EXCEPT HERE")
        img = cv2.imread('novideo.jpg')
        data = cv2.imencode('.jpg', img)[1].tobytes()
        return Response(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'
             + data 
             + b'\r\n\r\n', 
            mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
