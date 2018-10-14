from flask import Flask, request, jsonify, render_template
from utils.helper import colors
from collections import defaultdict
app = Flask(__name__)


boxes = defaultdict(dict)


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


@app.route('/boxes/<box_name>', methods=['GET', 'POST'])
def extend_box(box_name):
    if request.method == 'GET':
        if is_box_exist(box_name):
            print(boxes[box_name]['things'])
            return render_template('box_items.html', box_name=box_name,
                                   color=boxes[box_name]['color'],  things=boxes[box_name]['things'])

        else:
            return 'No boxes with {} name'.format(box_name), 404

    if request.method == 'POST':
        if is_box_exist(box_name):
            name = request.form['name']
            extend_boxes(box_name, name)
            return render_template('box_items.html', box_name=box_name,
                                   color=boxes[box_name]['color'], things=boxes[box_name]['things'])
        else:
            return 'No boxes with {} name'.format(box_name), 404


def create_box(name, color):
    boxes[name] = dict()
    boxes[name]['color'] = color
    boxes[name]['things'] = dict()


def is_box_exist(box_name):
    if box_name not in boxes.keys():
        return False
    return True


def extend_boxes(box_name, name):
    if name in boxes[box_name]['things'].keys():
        boxes[box_name]['things'][name] += 1
    else:
        boxes[box_name]['things'][name] = 1


if __name__ == '__main__':
    app.run(debug=True)
