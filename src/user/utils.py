import hashlib


def create_token(user_login):
    token = hashlib.sha256(user_login.encode()).hexdigest()
    return token