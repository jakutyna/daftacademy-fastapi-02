from hashlib import sha256

from fastapi import APIRouter, Depends, status, Response

from ..dependencies import authenticate, random_token

router = APIRouter(
    dependencies=[Depends(authenticate)]
)

router.session_token = None
router.login_token = None


@router.post('/login_session', status_code=status.HTTP_201_CREATED)
def login_session_view(response: Response):
    session_token = random_token()
    router.session_token = session_token
    response.set_cookie(key='session_token', value=session_token)
    return {'message': 'You are logged'}


@router.post('/login_token', status_code=status.HTTP_201_CREATED)
def login_session_view(response: Response):
    login_token = random_token()
    router.login_token = login_token
    return {'message': 'You are logged', "token": login_token}
