from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import os
import sys
from werkzeug.utils import secure_filename
from kof_to_csv import kof_to_csv_comma, kof_to_csv_period
from xml_to_csv import xml_to_csv_comma, xml_to_csv_period
from switch_xy import switch_points


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


app = Flask(__name__, template_folder=resource_path(
    'templates'), static_folder=resource_path('static'))

UPLOAD_FOLDER = resource_path('uploads')
ALLOWED_EXTENSIONS = {'kof', 'xml'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'action' not in request.form:
        return redirect(request.url)

    file = request.files['file']
    selected_action = request.form.get('action')
    selected_format = request.form.get('format')

    if file.filename == '' or not allowed_file(file.filename):
        return redirect(request.url)

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    file_extention = os.path.splitext(filename)[1].lower()
    base_name = os.path.splitext(filename)[0]

    if selected_action == 'change_format':
        if selected_format is None:
            return redirect(request.url)

        if selected_format == 'comma':
            csv_file = os.path.join(
                app.config['UPLOAD_FOLDER'], f'{base_name}_komma.office.csv')
            if file_extention == '.kof':
                kof_to_csv_comma(file_path, csv_file)
            elif file_extention == '.xml':
                xml_to_csv_comma(file_path, csv_file)
        else:
            csv_file = os.path.join(
                app.config['UPLOAD_FOLDER'], f'{base_name}_punktum.office.csv')
            if file_extention == '.kof':
                kof_to_csv_period(file_path, csv_file)
            elif file_extention == '.xml':
                xml_to_csv_period(file_path, csv_file)

        return jsonify({
            'csv_file': url_for('download_file', filename=os.path.basename(csv_file))
        })

    elif selected_action == 'switch_xy':
        if file_extention == '.xml':
            xml_file = os.path.join(
                app.config['UPLOAD_FOLDER'], f'{base_name}_xy.xml')
            switch_points(file_path, xml_file)
            return jsonify({
                'xml_file': url_for('download_file', filename=os.path.basename(xml_file))
            })
        else:
            return jsonify({'error': 'IREDES X & Y flipper er bare tillat for XML filer.'})


@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)


if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
