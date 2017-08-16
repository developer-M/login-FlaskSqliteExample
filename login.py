from flask import Flask
from flask_login import LoginManager, UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['DATABASE_FILE'] = 'data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SECRET_KEY'] = '123456790'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer,  primary_key=True )
    username = db.Column(db.String(30),  unique=True )

    def __init__(self, username ):
        self.username = username


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    user = User.query.filter_by(username='subie').first()
    login_user(user)
    return 'You are loged in ' + user.username


if __name__ == "__main__":
    app.run(debug=True)
