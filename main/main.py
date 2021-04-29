from datetime import date

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


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
