from .webapp_fastapi import socketio
from ib import IBManager

@socketio.on('Unsubscribe')
async def handle_unsubscribe(sid, *args, **kwargs):
    print('unsubscribe request received: ' + str(args))
    IBManager.getInstance().unsubscribeAll()

@socketio.on('Subscribe')
async def handle_subscribe(sid, *args, **kwargs):
    print('subscribe request received: ' + str(args))
    await IBManager.getInstance().batchsubscribe()

@socketio.on('connect_ib')
async def handle_connect(sid, *args, **kwargs):
    print('connect ib request received: ' + str(args))
    IBManager.getInstance().connectIB()
    IBManager.getInstance().setContract('AUDUSD')
    # IBManager.getInstance().connectIB('192.168.0.201',8000, 704)
    
@socketio.on('disconnect_ib')
async def handle_disconnect(sid, *args, **kwargs):
    print('disconnect ib request received: ' + str(args))
    IBManager.getInstance().close()

@socketio.on('my event')
async def handle_my_event(sid, *args, **kwargs):
    print(f'sid: {sid}')
    print(f'args: {args}')
    print(f'kwargs: {kwargs}')
    # print('received json: ' + str(json))
    await socketio.send("Message Recieved")

@socketio.on('join')
async def handle_join(sid, *args, **kwargs):
    await socketio.emit('lobby', 'User joined')