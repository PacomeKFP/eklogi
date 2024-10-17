import os
from flask import Flask, send_from_directory
from models import db
import config
from routes import router
import logging
from flask_migrate import Migrate


app = Flask(__name__)
app.register_blueprint(router)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = config.SECRET_KEY
db.init_app(app)
migrate = Migrate(app, db)


UPLOAD_FOLDER = 'uploads'


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    _logger = logging.Logger(__name__)

    if not os.path.exists(UPLOAD_FOLDER):
        _logger.warning("Directory for uploads not existing")
        os.makedirs(UPLOAD_FOLDER)
        _logger.info("Directory for uploads created")
    app.run(debug=True,port=80, host='0.0.0.0')
