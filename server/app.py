#!/usr/bin/env python3

from flask import request, session,make_response
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204
    
class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username']
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return make_response(user.to_dict(), 201)

    
class CheckSession(Resource):
    def get(self):
       user = User.query.filter(User.id == session['user_id']).first()
       if user:
           response = make_response(user.to_dict(),200)
           return response
       else:
           response = make_response({},204)
           return response

class Login(Resource):
    def post(self):
        user = User.query.filter_by(username = request.get_json()['username']).first()
        if user.authenticate(request.get_json()['password']):
            session['user_id'] = user.id
            response = make_response(user.to_dict(),201)
            return response

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        response = make_response({},204)
        return response

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
