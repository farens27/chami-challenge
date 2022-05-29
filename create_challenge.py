from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://chamidev:pi7890@36.89.148.117:3306/chamidb'
db = SQLAlchemy(app)

#Models Users Schema#
class Create_Challenge(db.Model):
    __tablename__ = "create_challenge"
    challenge_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(100))
    reward = db.Column(db.Integer)
    due_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    #due_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self, title, description, reward, due_date):
        self.title = title
        self.description = description
        self.reward = reward
        self.due_date = due_date  
    def __repr__(self):
        return '' % self.create_challenge  

db.create_all()
class Create_ChallengeSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Create_Challenge
        sqla_session = db.session
    #challenge_id = fields.Integer(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    reward = fields.String(required=True)
    due_date = fields.DateTime(required=True, format='%Y-%m-%dT%H:%M:%S%z')

@app.route('/create_challenge/')
def get_challenge():
	return jsonify([
		{ 
			'message': 'Berhasil Membuat Challenge',
            'status': 'true',
			'data': {
                'challenge_id' : Create_Challenge.challenge_id,
				'title': Create_Challenge.title,
				'description': Create_Challenge.description,
                'reward': Create_Challenge.reward,
                'due_date': Create_Challenge.due_date,
			}
		} for Create_Challenge in Create_Challenge.query.all()
	])
##get berdasarkan id#
#@app.route('/challenge/<challenge_id>/')
#def get_challenge(challenge_id):
#	print(challenge_id)
#	Create_Challenge = Create_Challenge.query.filter_by(public_id=challenge_id).first_or_404()
#	return jsonify([
#        {
#		'challenge_id': challenge_id.public_id, 
#        'tittle': challenge_id.tittle, 
#		'description': challenge_id.descri, 'is admin': user.
#		}
#    ])

@app.route('/create_challenge/', methods = ['POST'])
def create_challenge():
    data = request.get_json()
    create_challenge_schema = Create_ChallengeSchema()
    create_challenge = create_challenge_schema.load(data)
    result = create_challenge_schema.dump(create_challenge.create())
    return make_response(jsonify({"message":"berhasil tambah challenge", "create_challenge": result}),200)

@app.route('/Challenge', methods=['GET'])

def index():
    return jsonify({'message': 'Welcome to my API!'})


if __name__=='__main__':
    app.run(host="0.0.0.0", debug=True, port=80)