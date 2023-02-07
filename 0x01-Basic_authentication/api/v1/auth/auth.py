#!/usr/bin/env python3
'''Basic authentication module'''

from flask import request
from typing import List, TypeVar


class Auth:
    '''manage the API authentication'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''public method of Auth, returns boolean value'''
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        for paths in excluded_paths:
            if path.startwith(paths):
                return False
            if paths[-1] == '*':
                if path.startswith(paths[:-1]):
                    return False

    def authorization_header(self, request=None) -> str:
        ''' Auth public method that returns authorization header'''
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        '''Atho method that returns current user'''
        return None
