from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

pasta_raiz = app.root_path

app.config['SECRET_KEY'] = '16ec0e70e19528c516e0a890b93e496a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor faça login para acessar essa página'
login_manager.login_message_category = 'alert-info'

from comunidade import routes
