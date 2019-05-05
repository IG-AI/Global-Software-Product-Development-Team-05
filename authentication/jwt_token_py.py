import datetime
import jwt
JWT_SECRET = 'hasduiash79328jrej29r02r'

def encode(account):
    iat = datetime.datetime.utcnow()
    return jwt.encode({
        'sub': account['id'],
        'iat': iat,
        'exp': iat + datetime.timedelta(days=365)
    }, JWT_SECRET).decode('utf-8')

def hash(password):
    iat = datetime.datetime.utcnow()
    return jwt.encode({
        'sub': password,
        'iat': iat
    }, JWT_SECRET).decode('utf-8')


def decode(access_token):
    try:
        token = jwt.decode(access_token, JWT_SECRET, leeway=10)
    except jwt.InvalidTokenError:
        return None
    return token
