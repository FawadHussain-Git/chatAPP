from flask import Flask , render_template , request, redirect, url_for
from flask_socketio import SocketIO , join_room

app = Flask(__name__)
sio = SocketIO(app)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/chat')
def chat():
   username = request.args.get('username')
   room = request.args.get('room')
   if username and room:
        return render_template('chat.html',username = username,room=room)
   else:
        return redirect(url_for(home))

@sio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{0} has sent message to the room {1} : {2}".format(data['username'],data['room'],data['message']))
    sio.emit('receive_message',data,room=data['room'])

@sio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{0} has joined the room {1}".format(data['username'],data['room']))
    join_room(data['room'])
    sio.emit('join_room_announcement',data)


@sio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    sio.emit('leave_room_announcement', data, room=data['room'])

if __name__== "__main__":
    sio.run(app,debug = True)