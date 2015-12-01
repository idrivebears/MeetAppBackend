from flask import Flask, jsonify, make_response, request, g
import sqlite3
import requests
import json

from ma_models import *

app = Flask(__name__)

# Get the hardcoded DB :D
DATABASE = 'C:\Users\gwAwr\Documents\GitHub\MeetAppBackend\data\db\Meet.db'

# Add URI return for all objects

# get connection to database
def get_database():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db
# establish connection to database
def connect_to_database():
    con = None
    try:
        con = sqlite3.connect(DATABASE)
    except sqlite3.Error, e:
        print "fucking Error %s:" % e.args[0]
    return con;

# disconnect database on app context close
@app.teardown_appcontext
def teardown_request(self):
    db = getattr(g, '_database', None)

    if db is not None:
        db.close()

# Verify token with facebook
# Facebook verification: request https://graph.facebook.com/me?access_token=xxxxxxxxxxxxxxxxx
def verify_facebook_token(user_token):
    #Request verification of token from facebook
    facebook_response = requests.get("https://graph.facebook.com/me?access_token=%s" %  user_token).content

    #Should do some testing to make sure this works
    if facebook_response is None or "error" in facebook_response:
        return False
    return True

'''
URL ROUTING
'''

'''
GETTERS::::::::::::::::::::::::::::::::::::::::::::::::::::::::
'''
# Working
@app.route('/get/User/Info/<string:faceId>', methods=['GET'])
def get_user_Info(faceId):
    cur = get_database().cursor()
    args = (faceId, )
    cur.execute("""
                SELECT
                    MA_USER.Name,
                    MA_User.LastName,
                    MA_User.Birthdate,
                    MA_User.Gender,
                    Location.Latitude,
                    Location.Longitude
                FROM
                    MA_User,
                    Location
                WHERE
                    MA_User.IDLocation = Location.IDLocation AND
                    MA_User.FacebookID = ?
                """, args)
    query = cur.fetchall()
    print query
    user = User(query[0][0], query[0][1], query[0][2], query[0][3], faceId)
    return json.dumps(user.__dict__)

# Working
@app.route('/get/User/CreatedEvents/<string:faceId>', methods=['GET'])
def get_user_createdEvents(faceId):
    cur = get_database().cursor()
    args = (faceId, )
    cur.execute("""
                SELECT
            			Event.IDEvent AS 'EventID',
            			Event.Name AS 'EventName',
            			Place.Name AS 'PlaceName',
            			Event.DateTime AS 'EventDateTime'
            	FROM
            			MA_User
            			JOIN Event ON (MA_User.IDUser = Event.IDUser)
            			JOIN Place ON (Place.IDPlace = Event.IDPlace)
            	WHERE
            			MA_User.FacebookID = ?
            	ORDER BY
            			Event.DateTime DESC
                """, args)
    query = cur.fetchall()
    return jsonify({'Events:': query})

# Working
@app.route('/get/User/AttendedEvents/<string:faceId>', methods=['GET'])
def get_user_attendedEvents(faceId):
    cur = get_database().cursor()
    args = (faceId, )
    cur.execute("""
                SELECT
            			Event.IDEvent AS 'EventID',
            			Event.Name AS 'EventName',
            			Place.Name AS 'PlaceName',
            			Event.DateTime AS 'EventDateTime'
            	FROM
            			MA_User
            			JOIN MA_User_Event ON(MA_User.IDUser = MA_User_Event.IDUser)
            			JOIN Event ON (MA_User_Event.IDEvent = Event.IDEvent)
            			JOIN Place ON (Place.IDPlace = Event.IDPlace)
            	WHERE
            			Attendance = 1
            		AND MA_User.FacebookID = ?
            	ORDER BY
            			Event.DateTime DESC
                """, args)
    query = cur.fetchall()
    return jsonify({'Events': query})

# Working.
@app.route('/get/Place/Profile/<int:placeId>', methods=['GET'])
def get_place_profile(placeId):
    cur = get_database().cursor()
    args = (placeId, )
    cur.execute("""
                SELECT
            		Place.Name AS 'PlaceName',
            		Category.Name AS 'Category',
            		Place.Description AS 'PlaceDescription',
            		Location.Latitude,
            		Location.Longitude
                FROM
                		Place
                		JOIN Category ON (Category.IDCategory = Place.IDCategory)
                		JOIN Location ON (Location.IDLocation = PLACE.IDLocation)
                WHERE
                		Place.IDPlace = ?
                """, args)
    query = cur.fetchall()
    return jsonify({'Place': query})

# Working
@app.route('/get/User/Friends/<string:faceId>', methods=['Get'])
def get_user_friendList(faceId):
    cur = get_database().cursor()
    args = (faceId, )
    cur.execute("""
                SELECT
            			USER2.FacebookID,
            			USER2.Name,
            			USER2.LastName
            	FROM
            			MA_User AS USER1,
            			MA_User AS USER2,
            			MA_Users_Relation
            	WHERE
            			USER1.IDUser = MA_Users_Relation.IDUser_1
            		AND	USER2.IDUser = MA_Users_Relation.IDUser_2
            		AND	USER1.FacebookID = ?
            	ORDER BY
            			USER2.Name
                """, args)
    query = cur.fetchall()
    return jsonify({'Friends': query})

# Working
@app.route('/get/Events/<string:faceId>/<int:orderByRecommend>')
def getEvents(faceId, orderByRecommend):
    cur = get_database().cursor()
    args = (faceId, )
    if(orderByRecommend):
        cur.execute("""
                    SELECT	EventList.EventName,
            				EventList.EventDescription,
            				EventList.EventDateTime,
            				EventList.PlaceName,
            				MA_User.Name as 'CreatorFirstName',
            				MA_User.LastName as 'CreatorLastName'
            		FROM
            			(SELECT	Event.Name AS 'EventName',
            					Event.Description AS 'EventDescription',
            					Event.DateTime AS 'EventDateTime',
            					Place.Name AS 'PlaceName',
            					Event.IDUser AS 'IDCreatorUser',
            					Recommendation.Weight
            			FROM	MA_User,
            					Recommendation,
            					Event,
            					Place
            			WHERE	MA_User.IDUser = Recommendation.IDUser
            				AND	Event.IDEvent = Recommendation.IDEvent
            				AND MA_User.FacebookID = ?
            				AND Event.DateTime >= DATE('now', '-1 day') --CamNote: date function had to be mod for sqlite
            				AND	Place.IDPlace = Event.IDPlace) AS EventList,
            			MA_User
            		WHERE
            				MA_User.IDUser = EventList.IDCreatorUser
            		ORDER BY
            				EventList.Weight DESC
                    """, args)
    else:
        cur.execute("""
                    SELECT	EventList.EventName,
            				EventList.EventDescription,
            				EventList.EventDateTime,
            				EventList.PlaceName,
            				MA_User.Name AS 'CreatorFirstName',
            				MA_User.LastName AS 'CreatorLastName'
            		FROM
            			(SELECT	Event.Name AS 'EventName',
            					Event.Description AS 'EventDescription',
            					Event.DateTime AS 'EventDateTime',
            					Place.Name AS 'PlaceName',
            					Event.IDUser AS 'IDCreatorUser',
            					Recommendation.Weight
            			FROM	MA_User,
            					Recommendation,
            					Event,
            					Place
            			WHERE	MA_User.IDUser = Recommendation.IDUser
            				AND	Event.IDEvent = Recommendation.IDEvent
            				AND MA_User.FacebookID = ?
            				AND Event.DateTime >= DATE('now', '-1 day') --CamNote: date function had to be mod for sqlite
            				AND	Place.IDPlace = Event.IDPlace) AS EventList,
            			MA_User
            		WHERE
            				MA_User.IDUser = EventList.IDCreatorUser
            		ORDER BY
            				EventList.EventDateTime
                    """, args)
    query = cur.fetchall()
    return jsonify({'Events': query})

'''
CAMQUERIES -> SETTERS
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@app.route('/post/Event', methods=['POST'])
def create_event():
'''

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

if __name__ == '__main__':
    app.run(debug=True)
