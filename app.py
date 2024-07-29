from flask import Flask, request, render_template, send_from_directory
import qrcode
import os
from datetime import datetime

app = Flask(__name__)

# Define the static folder path
STATIC_FOLDER = 'static/images'
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            # Generate QR code
            img = qrcode.make(url)
            # Save the image with a unique name
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f'qr_{timestamp}.png'
            filepath = os.path.join(STATIC_FOLDER, filename)
            img.save(filepath)
            return render_template('index.html', filename=filename)
    return render_template('index.html', filename=None)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(STATIC_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
