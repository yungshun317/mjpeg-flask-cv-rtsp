from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

def generate_frames():
    """Generate Frame by Frame from Camera"""
    cam = cv2.VideoCapture("rtsp://localhost:8554/stream")

    while True:
        # Capture frame by frame
        ret, frame = cam.read()  # read the camera frame
        if not ret:
            break
        else:
            # Resize
            frame = cv2.resize(frame, (720, 720))

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video Streaming Route. Put this in the src attribute of an img tag."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/")
def index():
    """Video Streaming Home Page"""
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)