from flask import Flask, send_from_directory
from models import db
import config
from routes import router
from flask_env import MetaFlaskEnv


class Configuration(metaclass=MetaFlaskEnv):
    DEBUG = False
    PORT = 5000

app = Flask(__name__)
app.register_blueprint(router)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
app.config['SECRET_KEY'] = config.SECRET_KEY
db.init_app(app)

UPLOAD_FOLDER = 'uploads'

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)