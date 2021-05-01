from datetime import date

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')


# Ex1
@app.get('/hello', response_class=HTMLResponse)
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
@app.get('/hello2', response_class=HTMLResponse)
def hello2_view(request: Request):
    current_date = str(date.today())
    return templates.TemplateResponse("hello2.html", {"request": request, "current_date": current_date})
