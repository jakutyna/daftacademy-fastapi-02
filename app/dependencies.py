import random
import secrets
import string
from hashlib import sha256

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='app/templates')
security = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Gets and verifies credentials from 'authentication' header
    """
    correct_username = secrets.compare_digest(credentials.username, '4dm1n')
    correct_password = secrets.compare_digest(credentials.password, 'NotSoSecurePa$$')
    if not (correct_username and correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
    return credentials.username, credentials.password


def logout_json_html(query_params):
    """ Checks if there is 'format' in query parameters and returns response in correct format. """
    if 'format' in query_params:
        response_format = query_params['format']
        if response_format == 'json':
            return JSONResponse(content={'message': 'Logged out!'})
        elif response_format == 'html':
            return HTMLResponse(content='<h1>Logged out!</h1>')
    return PlainTextResponse(content='Logged out!')


def verify_token(tokens_cache, token):
    if token not in tokens_cache:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')


def random_token(token):
    # token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return sha256(token.encode()).hexdigest()


def response_json_html(query_params):
    if 'format' in query_params:
        response_format = query_params['format']
        if response_format == 'json':
            return JSONResponse(content={'message': 'Welcome!'})
        elif response_format == 'html':
            return HTMLResponse(content='<h1>Welcome!</h1>')
    return PlainTextResponse(content='Welcome!')
