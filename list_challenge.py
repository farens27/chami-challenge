from sqlalchemy.sql import func
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://chamidev:pi7890@36.89.148.117:3306/chamidb'
db = SQLAlchemy(app)

#Models Users Schema#
class List_Challenge(db.Model):
    __tablename__ = "list_challenge"
    challenge_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20))
    title = db.Column(db.String(20))
    description = db.Column(db.String(100))
    reward = db.Column(db.String(50))
    due_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    status = db.Column(db.String(20))
    is_winners = db.Column(db.String(30))
    winners = db.Column(db.String(30))

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self, title, user_id, description, reward, due_date, status, is_winners, winners):
        self.title = title
        self.user_id = user_id
        self.description = description
        self.reward = reward
        self.due_date = due_date
        self.status = status
        self.is_winners = is_winners
        self.winners = winners
    def __repr__(self):
        return '' % self.list_challenge  

db.create_all()
class List_ChallengeSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = List_Challenge
        sqla_session = db.session
    title = fields.String(required=True)
    user_id = fields.String(required=True)
    description = fields.String(required=True)
    reward = fields.Integer(required=True)
    due_date = fields.DateTime(required=True, format='%Y-%m-%dT%H:%M:%S%z')
    status = fields.String(required=True)
    is_winners = fields.String(required=True)
    winners = fields.String(required=True)

@app.route('/list_challenge/')
def get_list():
	return jsonify([
		{ 
			'message': 'Berhasil',
            'status': 'true',
			'data': {
                'challenge_id' : List_Challenge.challenge_id,
				'title': List_Challenge.title,
				'user_id': List_Challenge.user_id,
                'description': List_Challenge.description,
                'reward': List_Challenge.reward,
                'due_date' : List_Challenge.due_date,
				'status': List_Challenge.status,
				'is_winners': List_Challenge.is_winners,
                'winners': List_Challenge.winners,
			}
		} for List_Challenge in List_Challenge.query.all()
	])

@app.route('/list_challenge/', methods = ['POST'])
def list_challenge():
    data = request.get_json()
    list_challenge_schema = List_ChallengeSchema()
    list_challenge = list_challenge_schema.load(data)
    result = list_challenge_schema.dump(list_challenge.create())
    return make_response(jsonify({"message":"berhasil", "list_challenge": result}),200)

@app.route('/Challenge', methods=['GET'])

def index():
    return jsonify({'message': 'Welcome to my API!'})


if __name__=='__main__':
    app.run(host="0.0.0.0", debug=True, port=80)