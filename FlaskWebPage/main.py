from flask import Flask, render_template, Response
import cv2

camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame in the response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/integrantes")
def integrantes():
    return render_template("integrantes.html")

@app.route("/dash")
def dash():
    return render_template("dash.html")

@app.route("/video")
def video():
    return render_template("video.html")

@app.route('/video_feed')
def video_feed():
    # Return the response generated by the generate_frames() function
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

#@app.route("/visualização/<empresa>")
#def empresa(empresa):
#    return render_template("empresas.html", nome_empresa=empresa)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
