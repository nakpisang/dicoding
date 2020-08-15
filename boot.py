from flask import Flask
from flask_bootstrap import Bootstrap
import loader

app = Flask(__name__)
app.config.from_object('config')
bootstrap = Bootstrap(app)



loader.load(app)
