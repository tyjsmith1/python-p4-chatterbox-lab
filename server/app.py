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

@app.route('/messages',methods=['GET','POST'])
def messages():    
    if request.method == 'GET':
        messages = []
        bulk = Message.query.order_by(Message.created_at.asc()).all()
        for message in bulk:
            message_dict = message.to_dict()
            messages.append(message_dict)

        response = make_response(
            messages,
            200
        )
        return response
    elif request.method == 'POST':
        # new_message = Message(
        #     body = request.args.get("body"),
        #     username = request.agrs.get("username"),
        # )

        # db.session.add(new_message)
        # db.session.commit()

        # message_dict = new_message.to_dict()

        # response = make_response(
        #     message_dict,
        #     200
        # )
        # return response
        data = request.get_json()
        body = data['body']
        username = data['username']

        new_message = Message(
            body = body,
            username = username
        )

        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()

        return jsonify(message_dict), 201


@app.route('/messages/<int:id>', methods = ['PATCH','DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if request.method == 'PATCH':
        data = request.get_json()

        new_body = data['body']
        message.body = new_body

        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(
            message_dict,
            200
        )

        return response

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "message deleted."
        }

        response = make_response(
            response_body,
            200
        )

        return response

if __name__ == '__main__':
    app.run(port=5555)
