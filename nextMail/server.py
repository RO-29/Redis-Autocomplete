from flask import Flask, render_template,  send_from_directory, request
from flask_socketio import SocketIO
from flask_socketio import send, emit
from redis_util import RedisHelper
from ast import literal_eval

app = Flask(__name__)
socketio = SocketIO(app)

global bank_id_mapping_global; bank_id_mapping_global =  RedisHelper().get_redis_hash("bank_id_mapping")

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('get_bank_names')
def return_bank_names():
    bank_id_mapping = RedisHelper().get_redis_hash("bank_id_mapping")
    bank_names = bank_id_mapping.keys()
    emit('bank_names_recieve', bank_names)

@socketio.on('get_city_names')
def return_suggested_city_names(bank_name, city_keyword):
    city_keyword = city_keyword.upper()
    bank_id = bank_id_mapping_global.get(bank_name,"-")
    #import pdb;pdb.set_trace()
    
    #lexiographic search \xff --> \x hexadecimal, ff-255-highest word. 
    #Search through all city whose bankid:keyword matches till last lexigraphic order 
    min_str = "[{bank_id}:{city_keyword}".format(bank_id = bank_id, city_keyword = city_keyword)
    max_str = "[{bank_id}:{city_keyword}\xff".format(bank_id = bank_id, city_keyword = city_keyword)
    suggested_cities = RedisHelper().get_sorted_lex_string("autocompete", min_str, max_str)
    suggested_cities = [s_city.split("{bank_id}:".format(bank_id = bank_id))[1] for s_city in suggested_cities]
    emit('bank_city_recieve', suggested_cities)
    
    '''Earlier approach- get all bank-cities, search for the incoming pattern. inefficient, have to shift through all list-city
        return list of suggested cities based on city keyword recieved from user input
        suggested_cities = [city for city in city_names if city_keyword.lower() in city.lower()]
        emit('bank_city_recieve', suggested_cities)
    '''

@socketio.on('get_city_details')
def return_city_names(bank_name,city_name):
    bank_id = bank_id_mapping_global.get(bank_name,"-")
    city_details = RedisHelper().get_redis_hash(bank_id ,city_name)
    if city_details and city_details[0]:
        city_details = literal_eval(city_details[0])
    else:
        city_details = []
    emit('bank_city_details_recieve', city_details)




if __name__ == '__main__':
    socketio.run(app, host = '0.0.0.0')
