import os
import pdftotext
from flask import Flask, render_template, request, redirect, abort
from flask.helpers import send_from_directory
from werkzeug.exceptions import RequestedRangeNotSatisfiable
from werkzeug.utils import secure_filename
from nltk.tokenize import word_tokenize

import analyzer


app = Flask(__name__)

UPLOAD_FOLDER = app.root_path + ("\\uploads")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    text_from_pdf = None
    if request.method == 'POST':
        if request.method == "POST":
            if 'file' not in request.files:
                return redirect(request.url)
            file = request.files['file']
            if file.filename == "":
                return redirect(request.url)

            filename, file_extension = file.filename.split(".")

            if (file_extension != "pdf"):
                return redirect(request.url)

            if file:
                filename = secure_filename(file.filename)
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(upload_path)
                with open(upload_path, 'rb') as f:
                    pdf = pdftotext.PDF(f, "secret")
                    text_from_pdf = "\n".join(pdf)
                    analyzer.add_to_token(text_from_pdf, filename)

        return render_template('index.html', text_from_pdf=text_from_pdf)
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_req = request.form['search']
        search_request = word_tokenize(search_req)
        files = analyzer.search_files(search_request)
        return render_template('search.html', files=files, search_req=search_req)
    return render_template('search.html', gets=True, )


@app.route('/get_file/<filename>')
def fetch_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], path=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True, host='0.0.0.0')
