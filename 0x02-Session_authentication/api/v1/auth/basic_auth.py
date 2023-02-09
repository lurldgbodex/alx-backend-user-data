#!/usr/bin/env python3
'''basic authentication module'''

from .auth import Auth
import base64
import binascii
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    '''BasicAuth class inheriting from Auth class'''
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''returns base64 part of authorization
        header for basic authentication'''
        if authorization_header is None or type(
                                                  authorization_header) != str:
            return None

        if not authorization_header.startswith('Basic '):
            return None

        header_value = authorization_header.split(' ', 1)[1]
        return header_value

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        '''returns the decoded value of base64 string'''
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None

        try:
            auth_header_decoded = base64.b64decode(
                    base64_authorization_header,
                    validate=True).decode('utf-8')
            return auth_header_decoded
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        '''return user email and password from Base64 decoded value'''
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) != str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        user_credential = decoded_base64_authorization_header.split(':', 1)
        return tuple(user_credential)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        '''returns user instance based on his email and password'''
        if not isinstance(user_email, str):
            return None
        if not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''overloads auth current_user method and retrieves user
        instace of request'''
        auth_header = self.authorization_header(request)
        header_b64 = self.extract_base64_authorization_header(auth_header)
        header_decode = self.decode_base64_authorization_header(header_b64)
        email, password = self.extract_user_credentials(header_decode)
        return self.user_object_from_credentials(email, password)
