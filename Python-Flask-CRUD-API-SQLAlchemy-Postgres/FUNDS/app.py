from . import app,db
from flask import request, jsonify,make_response
from .models import Users,Funds
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy import func

@app.route('/signup', methods=['POST'])
def signup():
    # Signup logic here
    data = request.json
    email = data.get('email')
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    password = data.get('password')

    if firstName and lastName and email and password:
        # Save to database
        user=Users.query.filter_by(email=email).first()
        if user:
            return make_response({'message': 'Please Sign In'}, 200)
        user=Users(email=email,password=generate_password_hash(password),firstName=firstName,lastName=lastName)
        db.session.add(user)
        db.session.commit()
        return make_response({'message': 'User created successfully'}, 201)

    return make_response({'message': 'Unable to create User'}, 500)



@app.route('/login', methods=['POST'])
def login():
    auth=request.json
    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response({'message': 'Proper Credentials were not provided'}, 401)
    user=Users.query.filter_by(email=auth.get('email')).first()
    if not user:
        return make_response({'message': 'Please create an account'}, 404)
    if check_password_hash(user.password, auth.get('password')):
        token=jwt.encode({'id': user.id,'exp':datetime.utcnow()+timedelta(minutes=30)}, "secret","HS256")
        return make_response(jsonify({'token': token}), 201)
    return make_response('Please check your credentials', 401)


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token=None
        if 'Authorization' in request.headers:
            token=request.headers['Authorization']
        if not token:
            return make_response({'message': 'Token is missing'}, 401)
        
        try:
            data=jwt.decode(token, "secret", algorithms=["HS256"])
            current_user=Users.query.filter_by(id=data['id']).first()
            print(current_user)
        except Exception as e:
            print(e)
            return make_response({'message': 'Token is invalid'}, 401)
        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/funds', methods=['GET'])
@token_required
def getAllFunds(current_user):
    funds=Funds.query.filter_by(userId=current_user.id).all()
    totalSum=0
    if funds:
        totalSum+=Funds.query.with_entities(db.func.round(func.sum(Funds.amount),2)).filter_by(userId=current_user.id).all()[0][0]
    return make_response({"data": [row.serialize for row in funds], "Sum": totalSum}, 200)


@app.route('/funds', methods=['POST'])
@token_required
def createFund(current_user):
    data=request.json
    amount=data.get('amount')
    if amount:
        fund=Funds(amount=amount,userId=current_user.id)
        db.session.add(fund)
        db.session.commit()
    return fund.serialize





















































































































