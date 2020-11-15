from flask import Flask, render_template, request, redirect, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import firebase_admin
from firebase_admin import credentials
from pyfcm import FCMNotification


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clients.db'
db = SQLAlchemy(app)
cred = credentials.Certificate("тут была ссылка на файл")
firebase_admin.initialize_app(cred)
push_service = FCMNotification(api_key="тут был ключ")



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100),nullable=False)
    user = db.Column(db.String(100),nullable=False)
    password = db.Column(db.Integer, nullable=False)
    

    def __repr__(self):
        return 'User ' + str(self.id)

@app.route('/', methods=['GET', 'POST'])
def bank_users():
    
    if request.get_json():
        req = request.get_json()
        if (check_user(req.get("username"), req.get("password"))):
            response = {
                "success": "Login successful"
            }
        else:
            response = {
                "error": "Login failed"
            }
        res = make_response(jsonify(response), 200)
        return res
    else:
        req = request.headers
        res = make_response(jsonify({"error": "NO JSON recivied"}), 400)
        return res

def check_user(username, password):
    for user in User.query.filter_by(user=username).all():
        if (user.user == username) and (str(user.password) == password):
            return True
        else:
            return False
    


@app.route('/registration', methods=['POST'])
def register_user():
    if request.get_json(): 
        req = request.get_json()
        client_email = req.get('email')
        client_username = req.get('username')
        client_password = req.get('password')
        new_client = User(email=client_email, user=client_username, password = client_password)
        db.session.add(new_client)
        db.session.commit()
        response = {
                "success": "Registration successful"
            }
        res = make_response(jsonify(response), 200)
        return res
    else:
        res = make_response(jsonify({"error": "NO JSON recivied"}), 400)
        return res

@app.route('/push')
def push():
        registration_id = "тут был айди устройства"
        message_title = "Вот он мой пуш прекрасный"
        message_body = "Пуш долетел до цели успешно"
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
        return "PUSH отправлен"

    
if __name__ == "__main__":
    app.run(debug=True)