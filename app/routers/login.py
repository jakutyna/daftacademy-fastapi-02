from typing import Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException, status, Query, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse

from ..dependencies import authenticate, random_token, response_json_html

router = APIRouter(
    tags=['login'],
)

# # Tokens cached on server
# router.session_token = None
# router.login_token = None


# Ex2
@router.post('/login_session', status_code=status.HTTP_201_CREATED, dependencies=[Depends(authenticate)])
def login_session_view(response: Response):
    session_token = random_token()
    router.session_token = session_token
    response.set_cookie(key='session_token', value=session_token)
    return {'message': 'You are logged'}


@router.post('/login_token', status_code=status.HTTP_201_CREATED, dependencies=[Depends(authenticate)])
def login_session_view():
    json_token = random_token()
    router.json_token = json_token
    return {'message': 'You are logged', "token": json_token}


# Ex3
@router.get('/welcome_session')
def welcome_session_view(request: Request, session_token: Optional[str] = Cookie(None)):
    try:
        if session_token != router.session_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
    return response_json_html(request.query_params)


@router.get('/welcome_token')
def welcome_token_view(request: Request, token: Optional[str] = Query(None)):
    try:
        if token != router.json_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
    return response_json_html(request.query_params)


# View for testing authorization and 'Depends' method
@router.get('/login')
def login_view(cred: list = Depends(authenticate)):
    return {'user': cred[0], 'pass': cred[1]}
