from flask import Flask,jsonify,request

from config import Config
from models import User,db


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error':'not found','message':'Requested URL was not found on the server'}),404

@app.route('/users')
def users():
    users = User.query.all()
    users = [user.to_dict() for user in users]
    return jsonify(users)
    #return jsonify({'name':'ankit'})

@app.route('/users',methods=['POST'])
def create_users():
    data=request.get_json()
    new_user = User(username=data['username'],email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()),201  

@app.route('/users/<int:user_id>',methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route('/users/<int:user_id>',methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.username = data['username']
    user.email = data['email']
    db.session.commit()
    return jsonify(user.to_dict())

@app.route('/users/<int:user_id>',methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '',204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=5001)