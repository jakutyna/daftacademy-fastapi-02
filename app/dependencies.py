import random
import secrets
import string
from hashlib import sha256

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='app/templates')
security = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, '4dm1n')
    correct_password = secrets.compare_digest(credentials.password, 'NotSoSecurePa$$')
    if not (correct_username and correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')


def random_token():
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return sha256(token.encode()).hexdigest()
