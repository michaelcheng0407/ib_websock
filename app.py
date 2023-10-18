import nest_asyncio
nest_asyncio.apply()
import uvicorn
from typing import Optional
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse, RedirectResponse
from fastapi_socketio import SocketManager
from pydantic import BaseSettings
# from markupsafe import escape
import sqlite3
import ast
import json
import asyncio
from ib import IBManager
from ib_insync import *


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")
socketio = SocketManager(app=app)

# util.startLoop()

@app.get('/favicon.ico')
async def favicon():
    return FileResponse('favicon.ico')

@app.get('/', response_class=RedirectResponse)
async def index():
    return '/main'
    #return {"Hello": "World"}

@app.get('/hello', response_class=PlainTextResponse)
@app.get('/hello/{name}', response_class=PlainTextResponse)
async def hello(name=None):
    return f'Hello, {name}'

@app.get('/main/', response_class=HTMLResponse)
def main(request: Request):
    print(f"main load")
    # order_list= DBMgr.getOrders()
    # print(f"Orders: {order_list}")
    # print(type(order_list[0]))
    return FileResponse('templates/db_table.html')
    # return templates.TemplateResponse('db_table.html', {"request": request, "orders": order_list})

@app.get('/index/', response_class=HTMLResponse)
def index():
    return FileResponse('templates/index.html')





class DBMgr():
    def __init__(self):
        con = sqlite3.connect('testing.db')
        cur = con.cursor()
        DBMgr.create_table(con)
        con.commit()

    @staticmethod
    def create_table(con):
        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                ticker,
                order_action,
                order_contracts,
                order_price
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
	            Time DATETIME DEFAULT CURRENT_TIMESTAMP, 
                Ticker TEXT, 
                BuySell TEXT, 
                Quantity NUMERIC, 
                TarPrice NUMERIC
            )
        """)
        con.commit()

    @staticmethod
    def get_db():
        if not hasattr(app, 'db'): 
            print("app.db not exist")
            app.db = None
        if app.db is None:
            print("app.db is None")
            app.db = sqlite3.connect('testing.db')
        return app.db

    @staticmethod
    def getOrders():
        db = DBMgr.get_db()
        cursor = db.cursor()
        cursor.execute("""
            Select 
                Time,
                Ticker,
                Type,
                BuySell,
                Quantity,
                TarPrice,
                Type
            From Orders
        """
        )
        return cursor.fetchall()

def init_ib():
    ibmgr = IBManager.getInstance()
    ibmgr.setSM(socketio)
    # ibmgr.setContract('AUDUSD')
    # ibmgr.get_pos_list()
    # app.ibmgr.subscribeContract()

@app.on_event("startup")
async def startup_event():
    print("start up function called")
    # db = DBMgr()
    init_ib()
    # socketio.run(app)
    # ib_mgr.close()

@app.on_event("shutdown")
async def shutdown_event():
    IBManager.getInstance().close()
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

# Command to start the server in terminal
# uvicorn app:app --reload --port 5000