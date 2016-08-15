from flask import Flask, render_template,  send_from_directory, request
from flask_socketio import SocketIO
from flask_socketio import send, emit
from redis_util import RedisHelper

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('get_bank_names')
def return_bank_names():
    bank_names = RedisHelper().get_redis_list("bank_names")
    emit('bank_names_recieve', bank_names)

@socketio.on('get_city_names')
def return_city_names(bank_name):
    city_names = RedisHelper().get_redis_list(bank_name +'_city')
    emit('bank_city_recieve', city_names)

@socketio.on('get_city_details')
def return_city_names(bank_name,city_name):
    city_details = RedisHelper().get_redis_hash(bank_name ,city)
    emit('bank_city_details_recieve', city_details)

if __name__ == '__main__':
    socketio.run(app)
