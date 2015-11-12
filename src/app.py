from flask import Flask, jsonify, make_response, request, g
import sqlite3

app = Flask(__name__)

DATABASE = '/data/sql/database.db'
# Eventually:
# Remove testing 'database' add real database through flask
# Add URI return for all objects

################################ THE GREAT DATABASE #######################################
###########################################################################################
# Hard coded as fuck yo, abstract on to classes, handle everything through objects     ####
users = [
    {
        'user_id' : 1,
        'name' : 'Pedo',
        'lastname' : 'Lopez',
        'age' : 21,
    },
    {
        'user_id' : 2,
        'name' : 'Yoni',
        'lastname' : 'Elloko',
        'age' : 28,
    },
    {
        'user_id' : 3,
        'name' : 'Jaime',
        'lastname' : 'Rios',
        'age' : 23,
    }
]
events = [
    {
        'event_id' : 1,
        'name' : u'Peda en casa de pedo',
        'description' : u'Pos peda en casa de pedo caile',
        'creator_id' : 1,
        'guest_list' : [1, 2]
    },
    {
        'event_id' : 2,
        'name' : u'Maria se nos casa',
        'description' : u'Caiganle a la boda de Maria',
        'creator_id' : 1,
        'guest_list' : [1, 2]
    },
    {
        'event_id' : 3,
        'name' : u'All by myself pary',
        'description' : u'Alone alone',
        'creator_id' : 3,
        'guest_list' : [3]
    }
]
################################ THE GREAT DATABASE #######################################
###########################################################################################

'''
HERE BE DRAGONS
'''
@app.route('/get/event/list/<int:user_id>', methods=['GET'])
def get_eventlist(user_id):
    """Returns a list of all events the user can attend"""
    resultList = [event for event in events if user_id in event['guest_list']]
    return jsonify({'events':resultList})


@app.route('/post/event', methods=['POST'])
def create_event():
    """Creates a new event given the event name, and creator id"""
    if not request.json or not 'name' in request.json or not 'creator_id' in request.json:
        abort(400) #bad request bad bad request

    #literally using lists as objects at this point
    event = {
        'event_id' : events[-1]['event_id'] + 1,
        'name' : request.json['name'],
        'description' : request.json.get('description', ""),   #in case desc is empty
        'creator_id' : request.json['creator_id'],
        'guest_list' : [request.json['creator_id']]
    }

    events.append(event)
    return jsonify({'event': event}), 201                       #success


@app.errorhandler(404)
def not_found(error):
    """Return a 404 json instead of 404 html"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    return "<html><h1><a href='#'>Server running!</a></h1></html>"

def before_request():
    pass

def after_request():
    pass
    
if __name__ == '__main__':
    app.run(debug=True)
