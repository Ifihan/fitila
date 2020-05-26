from threading import Timer
import os
from urllib.parse import urljoin
from PIL import Image, ImageFont, ImageDraw
from flask import Flask, request, url_for, redirect


BASE_PATH = os.path.dirname(__file__)
STATIC_PATH = os.path.join(BASE_PATH, "static")
FONT_PATH = os.path.join(STATIC_PATH, "fonts")
CERTIFICATE_PATH = os.path.join(STATIC_PATH, "certificates")
GENERATED_PATH = os.path.join(STATIC_PATH, "generated")

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"


@app.route("/generate/")
def generate():
    certificate = make_certificate(**request.args)
    return redirect(certificate)


def delete_file(img_title):
    os.unlink(os.path.join(GENERATED_PATH, img_title))


def make_certificate(first_name, last_name, track):
    filename = "Fitila Certificate.png"
    font = "PTSans-Bold.ttf"
    color = "#ff0000"
    size = 50
    track_color = "#000000"
    track_size = 20
    y = 350
    x = 0

    text = "{} {}".format(first_name, last_name).upper()
    raw_img = Image.open(os.path.join(CERTIFICATE_PATH, filename))
    img = raw_img.copy()
    draw = ImageDraw.Draw(img)

    # draw name
    PIL_font = ImageFont.truetype(os.path.join(FONT_PATH, font), size)
    w, h = draw.textsize(text, font=PIL_font)
    W, H = img.size
    x = (W - w) / 2 if x == 0 else x
    draw.text((x, y), text, fill=color, font=PIL_font)

    # draw track
    PIL_font = ImageFont.truetype(os.path.join(FONT_PATH, font), track_size)
    w, h = draw.textsize(track, font=PIL_font)
    x, y = 183, 450
    draw.text((x, y), track, fill=track_color, font=PIL_font)

    img_title = "{}-{}-{}-30daysofcode.png".format(first_name, last_name, type)
    img.save(os.path.join(GENERATED_PATH, img_title))
    task = Timer(30, delete_file, (img_title,))
    task.start()
    base_64 =  urljoin(request.host_url, url_for("static", filename="generated/" + img_title))

    return base_64


if __name__ == "__main__":
    app.run(debug=True)
