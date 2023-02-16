#!/usr/bin/env python3
'''Auth module'''

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> str:
    '''return a salted hash of the input password'''
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    '''return a str rep of new uuid'''
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''Add a new user to db'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        '''returns true if password is valid else false'''
        try:
            user = self._db.find_user_by(email=email)
            user_password = user.hashed_password
            encoded_password = password.encode()
            valid_user = bcrypt.checkpw(encoded_password, user_password)
            if valid_user:
                return True
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        '''find the user corresponding to the email and generate
        a new uuid and store it in the database'''
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        ''' returns corresponding user or None'''
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        '''updates the corresponding user's session_id to None'''
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        '''find user corresponding to the email, and update
        the user's rest_token database field '''
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        '''use the reset_token to find the corresponding user,
        hash the password and update the user's hash_pw'''
        try:
            user = self._db.find_user_by(rest_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(
                user.id,
                hashed_password=hashed_password,
                reset_token=None
            )
        except NoResultFound:
            raise ValueError()
