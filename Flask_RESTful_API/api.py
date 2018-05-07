import jwt
from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
from flask_mail import Mail, Message
from flask_restful import abort, Api, Resource, reqparse, url_for
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize
app = Flask(__name__)
api = Api(app)
app.config.from_object('config_file')
parser = reqparse.RequestParser()
mail = Mail(app) # Must be after app.config

app.secret_key = app.config['SECRET_KEY'] # Otherwise flash does not work
msg_key = app.config['KEY'] # Encryption key for tokens

# Create database
db = SQLAlchemy(app)
class Users(db.Model):
    email = db.Column(db.String(30), primary_key=True) #A primary_key=True is necessary
    password = db.Column(db.String(15))
    active = db.Column(db.Boolean)

# Resources
class Signup(Resource):
    def post(self):
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        user_args = parser.parse_args() # Read input
        email = user_args['email']
        password = user_args['password']
        hash_password = generate_password_hash(password)
        user_db = Users(email=email, password=hash_password, active=0)
        # Add if email does not exist
        try:
            db.session.add(user_db)
            db.session.commit()
        except Exception as e:
            abort(401, message="It seems that this email address is occupied/nTry another one :)")
        token = jwt.encode({'email':email, 'password':hash_password}, msg_key, algorithm='HS256')
        link = url_for('activation', token=token, _external=True)
        msg_body = 'Welcome to our service. Your activation link is: {}'.format(link)#.format(token.decode('utf-8'))
        msg = Message(
        sender='sender@domain.com',# It is needed to manually lower the security settings of the sender's email account
        recipients=[email],
        subject='Activation code',
        body=msg_body)
        # In order to send the email you should: Manually lower the security settings for apps, in the sender's email account
        mail.send(msg)
        msg = (
        """Welcome to our place!
        Please search your emails...
        Activation key= %s""" % format(token.decode('utf-8'))) # The key is displayed for manual activation (for tests)
        return ({'message':msg})

class Activation(Resource):
    def post(self, token):
        # Uncheck the following 4 lines in order to insert a token manually (for tests)
        # Read input activation key from user
        # parser.add_argument('activation_key', type=str)
        # user_args = parser.parse_args()
        # token = user_args['activation_key']

        # Check activation key
        try:
            decoded_msg = jwt.decode(token, msg_key, algorithm='HS256')
        except jwt.DecodeError:
            abort(401, message='Activation key seems to be wrong')
        try:
            email = decoded_msg['email']
            # Search the user and activate account
            user = Users.query.get_or_404(email)
            user.active = True
            db.session.commit()
            return ({'message':str('Email: %s | Activated: %s' %(user.email, user.active))})
        except Exception:
            abort(401, message='Oops something went wrong, try again')
            return

class Login(Resource):
    def post(self):
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        user_args = parser.parse_args()
        email = user_args['email']
        password = user_args['password']
        # Check if the email exist or create an error if email is not in database
        try: # There is only one valid email, because of the checks during sign up
            user = Users.query.get_or_404(email)
        except Exception:
            abort(401, message='I am unable to find your email/nPlease Sign up')
        # Check if the password is correct
        if not check_password_hash(user.password, password):
            abort(401, message='Your password is incorrect')
        # Encode and return a token, if the check was successful
        if user.active == True:
            auth_token = jwt.encode({'email':email, 'check':True}, msg_key, algorithm='HS256')
            return {'token':auth_token.decode('utf-8')} # It is displayed for manual authorization (for tests)
        else:
            abort(401, message='Please activate your account. I will be here waiting for you!')
            return

def login_required(method):
    def wrapper(self):
        # Read header from postman ('Authorization, bearer <code>')
        try:
            header = request.headers.get('Authorization')
            _, token = header.split()
            decoded_token = jwt.decode(token, msg_key, algorithm='HS256')
            email = decoded_token['email']
            user = Users.query.get_or_404(email)
        except Exception:
            abort(400, message='Are you looking for something?')
        if not decoded_token['check'] == True:
            abort(400, message='Please log in or sign up')
        return method(self, user)
    return wrapper

class Main(Resource):
    @login_required
    def get(self, user):
        return str('Welcome! This message is for Active Members')

api.add_resource(Signup, '/signup', endpoint='signup') # 1
api.add_resource(Activation, '/activate/<token>', endpoint='activation') # 2
api.add_resource(Login, '/login', endpoint='login') # 3
api.add_resource(Main, '/main', endpoint='main') # 4

if __name__ == '__main__':
    app.run(debug=True) # Debug=True is needed for automatic re-run of the script
