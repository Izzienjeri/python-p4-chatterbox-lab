from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Hello, this is the root!"

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.order_by(Message.created_at).all()]
        response = make_response(jsonify(messages))
        return response

    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
        body=data.get("body"),
        username=data.get("username")
)

        
        db.session.add(new_message)
        db.session.commit()

        new_message_dict = new_message.to_dict()
        response = make_response(jsonify(new_message_dict), 200)
        return response

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    if not message:
        return make_response(jsonify({'error': 'Message not found'}), 404)

    if request.method == 'GET':
        message_dict = message.to_dict()
        response = make_response(jsonify(message_dict), 200)
        return response

    elif request.method == 'PATCH':
        message = Message.query.filter_by(id=id).first()
        for attr in request.json:
            setattr(message, attr, request.json[attr])

        db.session.add(message)
        db.session.commit()
        updated_message_dict = message.to_dict()
        response = make_response(jsonify(updated_message_dict), 200)
        return response

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Message deleted."
        }

        response = make_response(jsonify(response_body), 200)
        return response

if __name__ == '__main__':
    app.run(port=5555)
