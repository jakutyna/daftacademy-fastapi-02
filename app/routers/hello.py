from datetime import date
from typing import Optional

from fastapi import APIRouter, Header, Request
from fastapi.responses import HTMLResponse

from ..dependencies import templates

router = APIRouter(
    prefix='/hello',
    tags=['hello'],
)


# Ex1
@router.get('/', response_class=HTMLResponse)
def hello_view():
    return f"""
        <html>
            <head>
                <title>Hello with date</title>
            </head>
            <body>
                <h1>Hello! Today date is {str(date.today())}</h1>
            </body>
        </html>
        """


# Ex1 with templates
@router.get('/hello2', response_class=HTMLResponse)
def hello2_view(request: Request):
    current_date = str(date.today())
    return templates.TemplateResponse("hello2.html", {"request": request, "current_date": current_date})


# View for testing headers
@router.get('/headers')
# Typowanie na obiekt Header() spowoduje, że widok przechwici header o podanej nazwie (nazwie zmiennej)
def headers_view(request: Request, authorization: Optional[str] = Header(None), foo: Optional[str] = Header(None)):
    return {'authorization': authorization, 'foo': foo, 'request': str(request.headers)}
