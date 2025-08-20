from flask import Flask, render_template, request, send_file, redirect, url_for
from stego import LSBSteganographer, SteganographyException
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit
app.secret_key = os.urandom(24)

# CREATE DIRECTORY HERE - OUTSIDE THE if __name__ BLOCK
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/embed', methods=['POST'])
def embed():
    if 'file' not in request.files:
        return render_template('error.html', error="No file selected")

    file = request.files['file']
    message = request.form.get('message', '')
    key = request.form.get('key', '0x1A')

    if not message:
        return render_template('error.html', error="No message provided")

    try:
        key = int(key, 16) if key.startswith('0x') else int(key)
    except ValueError:
        return render_template('error.html', error="Invalid encryption key format")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encoded_' + filename)

        # Ensure directory exists (backup safety check)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        file.save(input_path)

        try:
            stego = LSBSteganographer()
            stego.embed_data(input_path, message, output_path, key)
            return send_file(output_path, as_attachment=True)
        except SteganographyException as e:
            return render_template('error.html', error=str(e))
        finally:
            if os.path.exists(input_path):
                os.remove(input_path)
            if os.path.exists(output_path):
                os.remove(output_path)

    return render_template('error.html', error="Invalid file type")

@app.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return render_template('error.html', error="No file selected")

    file = request.files['file']
    key = request.form.get('key', '0x1A')

    try:
        key = int(key, 16) if key.startswith('0x') else int(key)
    except ValueError:
        return render_template('error.html', error="Invalid encryption key format")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Ensure directory exists (backup safety check)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        file.save(file_path)

        try:
            stego = LSBSteganographer()
            message = stego.extract_data(file_path, key)
            return render_template('result.html', message=message)
        except SteganographyException as e:
            return render_template('error.html', error=str(e))
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    return render_template('error.html', error="Invalid file type")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
