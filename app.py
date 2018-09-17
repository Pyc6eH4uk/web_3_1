from flask import Flask, request, jsonify, render_template
from utils.helper import colors

app = Flask(__name__)


boxes = dict()


@app.route('/')
def index():
    return render_template('index.html', boxes=boxes)


@app.route('/boxes', methods=['GET', 'POST'])
def available_boxes():
    if request.method == 'GET':
        return render_template('boxes.html', boxes=boxes)

    if request.method == 'POST':
        name = request.form['name']
        color = request.form['color']
        if color not in colors:
            error = 'You can not add box with such color: {}'.format(color)
            return render_template('boxes.html', boxes=boxes, error=error)
        if color not in boxes.values() and name not in boxes.keys():
            create_box(name, color)
            happy = 'We add your box to our storage.'
            return render_template('boxes.html', boxes=boxes, happy=happy)
        else:
            error = 'Box with such color or name already exist.'
            return render_template('boxes.html', boxes=boxes, error=error)


def create_box(name, color):
    print(name, color)
    boxes[name] = color


if __name__ == '__main__':
    app.run(debug=True)