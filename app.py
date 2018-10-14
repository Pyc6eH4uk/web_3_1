from flask import Flask, request, session, render_template, url_for, redirect
from utils.helper import colors
from collections import defaultdict
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

users = ['user1', 'user2', 'user3']
boxes = defaultdict(dict)


@app.route('/')
def index():
    return render_template('index.html', boxes=boxes)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        print(session)
        return render_template('login.html')

    if request.method == 'POST':
        session['user'] = request.form['name']
        return redirect(url_for('index'))


@app.route('/boxes', methods=['GET', 'POST'])
def available_boxes():
    if request.method == 'GET':
        print(session)
        return render_template('boxes.html', boxes=boxes)

    if request.method == 'POST':
        name = request.form['name']
        color = request.form['color']
        print(session)
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


@app.route('/boxes/<box_name>', methods=['GET', 'PUT'])
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
            if session['user'] == boxes[box_name]['creator']:
                name = request.form['name']
                extend_boxes(box_name, name)
                return render_template('box_items.html', box_name=box_name,
                                       color=boxes[box_name]['color'], things=boxes[box_name]['things'])
            else:
                return 'Restricted access', 400
        else:
            return 'No boxes with {} name'.format(box_name), 404


def create_box(name, color):
    boxes[name] = dict()
    boxes[name]['color'] = color
    boxes[name]['creator'] = session['user']
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
