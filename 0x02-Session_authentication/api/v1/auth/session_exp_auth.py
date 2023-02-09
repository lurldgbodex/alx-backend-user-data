#!/usr/bin/env python3
'''session authentication exp module'''

from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    '''session auth expiration'''
    def __init__(self):
        '''class constructor for SessionExpAuth'''
        try:
            session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            session_duration = 0

        self.session_duration = session_duration

    def create_session(self, user_id=None):
        '''create session id for user'''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
                'user_id': user_id,
                'created_at': datetime.now()
                }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''retrieves user_id from a session'''
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')

        created_at = session_dictionary.get('created_at')
        if created_at is None:
            return None
        exp_time = created_at + timedelta(seconds=self.session_duration)
        if exp_time < datetime.now():
            return None
        return session_dictionary.get('user_id')
