
## Warning 
Do not use any of the code in this repo for trading. It is not completed with lots of bugs

# Proof of concept App for giving IB TWS a frontend with ib_inysnc aand websocket
This project implements a web app for interactive stock charting and trading via FastAPI, SocketIO, ib_insync.

## Overview
The app consists of:
- A FastAPI backend with websockets using SocketIO.
- An Interactive Brokers wrapper using ib_insync for market data and trade execution.
- A frontend built with HTML, CSS, JavaScript and minimal vue.js .

## Key features:
- Real-time charting of market data streamed from IB.
- Submit trade orders to IB which are executed automatically.
- Manage open positions and portfolio. (not complete)
- Store trade signals and orders in a local SQLite database. (not complete)

