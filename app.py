from flask import Flask, render_template, request, redirect, url_for
import os
from mask_generator import generate_masks

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MASK_FOLDER'] = 'static/masks'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['MASK_FOLDER']):
    os.makedirs(app.config['MASK_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Call the function to create masks
            masks_path = generate_masks(filepath, app.config['MASK_FOLDER'])

            return redirect(url_for('uploaded_file', filename=filename, masks_path=masks_path))
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    masks_path = request.args.get('masks_path', None)
    return render_template('display.html', filename=filename, masks_path=masks_path)

if __name__ == '__main__':
    app.run(debug=True)
