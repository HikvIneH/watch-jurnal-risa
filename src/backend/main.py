import html
import socketio

socket = socketio.Server()

connections = []
usernames = {}
roomusers = {}


@socket.on('connect')
def connect(sid, environ):
    print('connect ', sid)
    connections.append(str(sid))
    print('connected sockets: ', len(connections))


@socket.on('join room')
def join_room(sid, roomnum, username="Aditya"):
    for room in socket.rooms(sid):
        socket.leave_room(sid, room)
    usernames[str(sid)] = html.escape(str(username))
    socket.enter_room(sid, roomnum)
    room = str(socket.rooms(sid)[0])
    if type(roomusers.get(room)) == list:
        roomusers[room].append(usernames.get(str(sid), "Aditya"))
    else:
        roomusers[room] = []
        roomusers[room].append(usernames.get(str(sid), "Aditya"))
    data = roomusers.get(room)
    socket.emit('get users', data, room=room)


@socket.on('play video')
def play_video(sid, data):
    room = str(socket.rooms(sid)[0])
    data = {
        "state": data.get("state", ""),
    }
    socket.emit('play video client', data, room=room)


@socket.on('sync video')
def sync_video(sid, data):
    room = str(socket.rooms(sid)[0])
    data = {
        "time": data.get("time"),
        "state": data.get("state"),
        "videoId": data.get("videoId"),
    }
    socket.emit('sync video client', data, room=room)


@socket.on('change video')
def change_video(sid, data):
    room = str(socket.rooms(sid)[0])
    data = {
        "videoId": data.get("videoId"),
    }
    socket.emit('change video client', data, room=room)


@socket.on('')
def fname(sid):
    pass


@socket.on('')
def fname(sid):
    pass


@socket.on('disconnect')
def disconnect(sid):
    room = str(socket.rooms(sid)[0])
    if room in roomusers:
        roomusers[room].remove(usernames.get(str(sid)))
    socket.emit('get users', roomusers.get(room), room=room)
    for uroom in socket.rooms(sid):
        socket.leave_room(sid, uroom)
    if str(sid) in usernames:
        del(usernames[str(sid)])
        connections.remove(str(sid))
    print('disconnect ', sid)
    print('connected sockets: ', len(connections))
