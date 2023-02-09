#!/usr/bin/env python3
'''session Authentication'''

from .auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    '''class SessionAuth inherits from Auth class'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''creates a session id for a user_id'''
        if user_id is None or type(user_id) != str:
            return None
        else:
            session_id = str(uuid4())
            self.user_id_by_session_id = {
                    session_id: user_id
                    }
            return session_id
