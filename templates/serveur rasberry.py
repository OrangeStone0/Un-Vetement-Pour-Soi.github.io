from flask import Flask, request, render_template
from flask import Flask, render_template, Response, url_for
import cv2
from flask import Flask, render_template, jsonify
import time
import random
import numpy as np

app = Flask(__name__, static_url_path='/static')

# Utilitaire pour capturer le flux vidéo de la webcam
def generate_frames():
    camera = cv2.VideoCapture(0)  # 0 pour la webcam intégrée, changez-le si vous avez une webcam externe

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()
@app.route('/')
def accueil():
    return render_template('accueil.html')
@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/button_pressed', methods=['POST'])
def button_pressed():
    data = request.get_json()
    button_number = data.get('button')
    print(f'Bouton pressé : {button_number}')
    return 'OK'

@app.route('/mise_a_jour')
def mise_a_jour():
    # Exemple de données mises à jour côté serveur
    texte_flask = str(random.randint(1, 99))
    return jsonify({'texte_flask': texte_flask})

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
