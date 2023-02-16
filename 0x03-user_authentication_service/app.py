#!/usr/bin/env python3
'''app module'''

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
Auth = Auth()


@app.route('/', methods=['GET'])
def index() -> str:
    '''return a Json payload'''
    return jsonify({
        "message": "Bienvenue"
    })


@app.route('/users', methods=['POST'])
def post_user() -> str:
    '''post a new user'''
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        user = Auth.register_user(email, password)
        return jsonify({
            "email": email,
            "message": "user created"
        })
    except ValueError:
        return jsonify({
            "message": "email already registered"
        }), 400
    except


@app.route('/sessions', methods=['POST'])
def login() -> str:
    '''respond to the POST /sessions route'''
    email = requests.form.get('email')
    password = requests.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    res = jsonify({
        "email": email,
        "message": "logged in"
    })
    res.set_cookie("session_id", session_id)
    return res


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    '''deletes session and redirects to home route'''
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile')
def get_profile() -> str:
    '''get /profile and return user's profile info'''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({
        "email": user.email
    })


@app.route('/reset_password', methods=['POST'])
def reset_password() -> str:
    ''' return user's password reset pasyload'''
    email = request.form.get('email')
    reset_token = None
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({
            "email": email,
            "reset_token": reset_token
        }), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    ''' return user's password updated payload'''
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = reques.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({
            "email": email,
            "message": "Password updated"
        }), 200
    except ValueError:
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
