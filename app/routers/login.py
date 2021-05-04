from typing import Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException, status, Query, Request, Response
from fastapi.responses import RedirectResponse

from ..dependencies import authenticate, logout_json_html, random_token, response_json_html, verify_token

router = APIRouter(
    tags=['login'],
)

# Tokens cached on server
router.session_tokens = []
router.json_tokens = []


# Ex2
@router.post('/login_session', status_code=status.HTTP_201_CREATED, dependencies=[Depends(authenticate)])
def login_session_view(response: Response):
    """ Verifies credentials and generates random session token kept in cookie. """
    session_token = random_token()
    router.session_tokens.append(session_token)
    if len(router.session_tokens) > 3:
        del router.session_tokens[0]
    response.set_cookie(key='session_token', value=session_token)
    return {'message': 'You are logged'}


@router.post('/login_token', status_code=status.HTTP_201_CREATED, dependencies=[Depends(authenticate)])
def login_session_view():
    """ Verifies credentials and generates random session token kept in json file. """
    json_token = random_token()
    router.json_tokens.append(json_token)
    if len(router.json_tokens) > 3:
        del router.json_tokens[0]
    return {'message': 'You are logged', "token": json_token}


# Ex3
@router.get('/welcome_session')
def welcome_session_view(request: Request, session_token: Optional[str] = Cookie(None)):
    verify_token(router.session_tokens, session_token)
    return response_json_html(request.query_params)


@router.get('/welcome_token')
def welcome_token_view(request: Request, token: Optional[str] = Query(None)):
    verify_token(router.json_tokens, token)
    return response_json_html(request.query_params)


# Ex4
@router.delete('/logout_session')
def logout_session_view(request: Request, session_token: Optional[str] = Cookie(None)):
    verify_token(router.session_tokens, session_token)
    router.session_tokens.remove(session_token)
    url = f'/logged_out?format={request.query_params["format"]}' if 'format' in request.query_params else '/logged_out'
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@router.delete('/logout_token')
def logout_token_view(request: Request, token: Optional[str] = Query(None)):
    verify_token(router.json_tokens, token)
    router.json_tokens.remove(token)
    url = f'/logged_out?format={request.query_params["format"]}' if 'format' in request.query_params else '/logged_out'
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@router.get('/logged_out')
def logout_session_view(request: Request):
    return logout_json_html(request.query_params)


# View for testing authorization and 'Depends' method
@router.get('/login')
def login_view(cred: list = Depends(authenticate)):
    return {'user': cred[0], 'pass': cred[1]}
