import os
from flask import Flask, request, render_template

from src import ImageCaptionGenerator
from src.logger import logging

# import logging
# logging.basicConfig(level=logging.INFO, format='%(process)d-%(levelname)s-%(message)s')

application=Flask(__name__)

app=application

# configuring the upload folder
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    img_cap_gen = ImageCaptionGenerator()
    url = request.form.get("imgUrl")
    uploaded_file = request.files.get('file')
    n_captions = int(request.form.get("n_capt")) - 1

    logging.info(f"Number of captions will be generated: {n_captions + 1}")

    if url:
        logging.info("Got a url")
        logging.info("generating captions...")
        gen_captions = img_cap_gen.generate_caption(url, n_captions)

    if uploaded_file:
        logging.info("Got a file")
        upload_file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(upload_file_path)
        logging.info("generating captions...")
        gen_captions = img_cap_gen.generate_caption(upload_file_path, n_captions)

    logging.info(f"Generated Captions are: {gen_captions}")

    return {"captions": gen_captions}


if __name__ == "__main__":
    app.run()
