from flask import Flask
from flask_migrate import Migrate
from models import db
import config
from routes import router
import pymysql


app = Flask(__name__)
app.register_blueprint(router)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
app.config['SECRET_KEY'] = config.SECRET_KEY
db.init_app(app)

pymysql.install_as_MySQLdb()


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

