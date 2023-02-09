#!/usr/bin/env python3
""" Module of Session in Database
"""
from .session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session in database Class"""

    def create_session(self, user_id=None):
        """Creation session database"""
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        kwargs = {
                'user_id': user_id,
                'session_id': session_id
                }
        user_session = UserSession(**kwargs)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """User ID for Session ID Database"""
        if session_id is None:
            return None

        try:
            user_session = UserSession.search({
                'session_id': session_id
                })
        except Exception:
            return None
        session = user_session[0]
        time_span = timedelta(seconds=self.session_duration)
        exp_time = session.created_at + time_span
        if exp_time < datetime.now():
            return None
        return session.user_id

    def destroy_session(self, request=None):
        """Remove Session from Database"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_session = UserSession.search({
            'session_id': session_id
            })

        if not user_session:
            return False

        session = user_session[0]

        try:
            session.remove()
        except Exception:
            return False
        return True
