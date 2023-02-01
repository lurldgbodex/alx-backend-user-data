#!/usr/bin/env python3
'''personal data'''

import bcrypt


def hash_password(password: str) -> bytes:
    '''returns a salted hashed password'''
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''validates password and hashed_password'''
    validity = bcrypt.checkpw(password.encode(), hashed_password)
    return validity
