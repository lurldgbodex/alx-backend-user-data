#!/usr/bin/env python3
'''session authentication module'''

from api.v1.views import app_views as a_v
from flask import jsonify, abort, request
from models.user import User
import os
from api.v1.app import auth


@a_v.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def handle_session_authentication_login():
    '''a post method that handles all routes for session authentication'''
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({'error': 'email missing'}), 400
    if not password:
        return jsonify({'error': 'password missing'}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({'error': 'no user found for this email'}), 404
    user = users[0]
    if user.is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        cookie_name = os.getenv('SESSION_NAME')
        response = jsonify(user.to_json())
        response.set_cookie(cookie_name, session_id)
        return response
    return jsonify({'error': 'wrong password'}), 401


@a_v.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def handle_session_authentication_logout():
    '''handle session auth logout'''
    is_destroyed = auth.destroy_session(request)
    if not destroyed:
        abort(404)
    return jsonify({}), 200
