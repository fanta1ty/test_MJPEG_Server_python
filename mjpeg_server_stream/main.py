import cv2
from flask import Flask, Response

app = Flask(__name__)

# Path to the MP4 video file
VIDEO_SOURCE = 'shaky_video.mp4'  # Replace 'video.mp4' with the full path to your MP4 file


def generate_mjpeg():
    # Open the video file
    video = cv2.VideoCapture(VIDEO_SOURCE)
    if not video.isOpened():
        print("Error: Could not open video file.")
        return

    while True:
        success, frame = video.read()  # Read the next frame
        if not success:  # Restart video when it ends
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Send the frame in MJPEG format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    video.release()


@app.route('/mjpeg')
def mjpeg_stream():
    return Response(generate_mjpeg(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)
