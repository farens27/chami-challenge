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
class Submit_Challenge(db.Model):
    __tablename__ = "submit_challenge"
    challenge_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20))
    file = db.Column(db.String(20))
    pesan = db.Column(db.String(100))

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self, user_id, file, pesan):
        self.user_id = user_id
        self.file = file
        self.pesan = pesan
    def __repr__(self):
        return '' % self.submit_challenge  

db.create_all()
class Submit_ChallengeSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Submit_Challenge
        sqla_session = db.session
    user_id = fields.String(required=True)
    file = fields.String(required=True)
    pesan = fields.String(required=True)

@app.route('/submit_challenge/')
def get_submit():
	return jsonify([
		{ 
			'message': 'Berhasil Submit Challenge',
            'status': 'true',
			'data': {
                'challenge_id' : Submit_Challenge.challenge_id,
                'user_id' : Submit_Challenge.user_id,
				'file': Submit_Challenge.file,
				'pesan': Submit_Challenge.pesan,
			}
		} for Submit_Challenge in Submit_Challenge.query.all()
	])

@app.route('/submit_challenge/', methods = ['POST'])
def submit_challenge():
    data = request.get_json()
    submit_challenge_schema = Submit_ChallengeSchema()
    submit_challenge = submit_challenge_schema.load(data)
    result = submit_challenge_schema.dump(submit_challenge.create())
    return make_response(jsonify({"message":"berhasil submit challenge", "submit_challenge": result}),200)

@app.route('/Challenge', methods=['GET'])

def index():
    return jsonify({'message': 'Welcome to my API!'})


if __name__=='__main__':
    app.run(host="0.0.0.0", debug=True, port=80)