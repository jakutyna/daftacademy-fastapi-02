from typing import Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException, status, Query, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse

from ..dependencies import authenticate, random_token, response_json_html, logout_json_html

router = APIRouter(
    tags=['login'],
)

# Tokens cached on server
router.session_token = []
router.json_token = []


# Ex2
@router.post('/login_session', status_code=status.HTTP_201_CREATED, dependencies=[Depends(authenticate)])
def login_session_view(response: Response):
    session_token = random_token()
    if len(router.session_token) == 0:
        router.session_token.append(session_token)
    else:
        router.session_token[0] = session_token
    response.set_cookie(key='session_token', value=session_token)
    return {'message': 'You are logged'}


@router.post('/login_token', status_code=status.HTTP_201_CREATED, dependencies=[Depends(authenticate)])
def login_session_view():
    json_token = random_token()
    if len(router.json_token) == 0:
        router.json_token.append(json_token)
    else:
        router.json_token[0] = json_token
    return {'message': 'You are logged', "token": json_token}


# Ex3
@router.get('/welcome_session')
def welcome_session_view(request: Request, session_token: Optional[str] = Cookie(None)):
    try:
        if session_token != router.session_token[0]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
    except IndexError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
    return response_json_html(request.query_params)


@router.get('/welcome_token')
def welcome_token_view(request: Request, token: Optional[str] = Query(None)):
    try:
        if token != router.json_token[0]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
    except IndexError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
    return response_json_html(request.query_params)


# Ex4
@router.delete('/logout_session')
def logout_session_view(request: Request, session_token: Optional[str] = Cookie(None)):
    try:
        if session_token != router.session_token[0]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
    except IndexError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
    del router.session_token[0]
    url = f'/logged_out?format={request.query_params["format"]}' if 'format' in request.query_params else '/logged_out'
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@router.delete('/logout_token')
def logout_token_view(request: Request, token: Optional[str] = Query(None)):
    try:
        if token != router.json_token[0]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
    except IndexError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized')
    del router.json_token[0]
    url = f'/logged_out?format={request.query_params["format"]}' if 'format' in request.query_params else '/logged_out'
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@router.get('/logged_out')
def logout_session_view(request: Request):
    return logout_json_html(request.query_params)


# View for testing authorization and 'Depends' method
@router.get('/login')
def login_view(cred: list = Depends(authenticate)):
    return {'user': cred[0], 'pass': cred[1]}
