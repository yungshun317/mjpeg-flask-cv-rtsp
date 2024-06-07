from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

cam = cv2.VideoCapture("rtsp://localhost:8554/stream")

def gen_frames():
    """Generate Frame by Frame from Camera"""
    while True:
        # Capture frame by frame
        ret, frame = cam.read()  # read the camera frame
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video Streaming Route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/")
def index():
    """Video Streaming Home Page"""
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)