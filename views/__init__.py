from PIL import Image
from flask import Flask, Blueprint, render_template, request, jsonify, redirect, url_for, g, session
from torch_mtcnn import detect_faces
from flask_bootstrap import Bootstrap
from util import is_same, ModelLoaded


base = Blueprint('base', __name__, template_folder='templates')
THRESHOLD = 1.5
# bootstrap = Bootstrap(base)


@base.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='nakpisang', password='password'))
users.append(User(id=2, username='zul', password='password'))
users.append(User(id=3, username='rizal', password='password'))
users.append(User(id=4, username='admin', password='password'))

@base.route('/index')
def index():
    return render_template('index.html')

@base.route('/home')
def home():
    return render_template('indexx.html')


@base.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id

            return redirect(url_for('base.home'))

        return redirect(url_for('base.login'))

    return render_template('loginn.html')


@base.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('base.login'))

@base.route('/predict', methods=['post'])
def predict():
    files = request.files
    img_left = Image.open(files.get('imgLeft')).convert('RGB')
    img_right = Image.open(files.get('imgRight')).convert('RGB')
    bbox_left, _ = detect_faces(img_left)
    bbox_right, _ = detect_faces(img_right)
    if bbox_left.shape[0] > 0:
        a, b, c, d, _ = bbox_left[0]
        img_left = img_left.crop((a, b, c, d))
    if bbox_right.shape[0] > 0:
        a, b, c, d, _ = bbox_right[0]
        img_right = img_right.crop((a, b, c, d))
    distance, similar = is_same(img_left, img_right, THRESHOLD)
    model_acc = ModelLoaded.acc
    return jsonify(same=('BERBEDA', 'SAMA')[similar.item()],
                   score=distance.item(),
                   model_acc=model_acc,
                   threshold=THRESHOLD)

