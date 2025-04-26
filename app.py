from flask import Flask, request, render_template, jsonify
import numpy as np
import tensorflow as tf
from PIL import Image
import io
import os

app = Flask(__name__)
model = tf.keras.models.load_model('blood_group_model.h5')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})

    mode = request.form.get('mode')  # Check if user selected real-time mode

    try:
        image = Image.open(io.BytesIO(file.read())).convert('RGB')

        # For real-time screenshot input: resize to 64x64 to match model input
        if mode == 'realtime':
            image = image.resize((64, 64))
        else:
            image = image.resize((64, 64))

        img_array = np.expand_dims(np.array(image) / 255.0, axis=0)
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction)
        confidence = np.max(prediction) * 100

        blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        correct_mapping = [0, 1, 4, 5, 2, 3, 6, 7]
        result = blood_groups[correct_mapping[predicted_class]]

        return jsonify({'prediction': result, 'confidence': f'{confidence:.2f}%'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
