from flask import Flask
from routes import routes
from models import db # Importe l'instance de base de données depuis models.py
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'une_cle_secrete_tres_secrete'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'routes.login'
login_manager.login_message_category = 'info'
login_manager.init_app(app)

app.register_blueprint(routes)

from models import User, Patient, AnalyseResult # noqa

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_database():
    with app.app_context():
        db.create_all()
        print('Base de données créée!')

if __name__ == '__main__':
    create_database()
    app.run(debug=True)