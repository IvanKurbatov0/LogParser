from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import Parser
import os


ALLOWED_EXTENSIONS = {'bin'}
UPLOAD_FOLDER = 'log'


app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return "Upload file"


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        try:
            if os.path.exists('log.bin'):
                os.remove('log.bin')
        except Exception as e:
            print(e)
        if request.files['file']:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename('log.bin')
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                try:
                    log = Parser.read('log/log.bin')
                    Parser.GetGameDescriptionPlayers(log)
                    Parser.GetGameDescriptionPolygon(log)
                    Parser.SetServerClass(Parser.GetServerEvent(log))
                    Parser.SetPlayerClass(Parser.GetPlayersEvent(log),
                                          Parser.GetDataPlayers(log))
                    Parser.SetPolygonClass(Parser.GetPolygonLog(log))
                except Exception as e:
                    print(e)
                    return 'Error Parser'
                return 'File uploaded successfully'
            return 'File upload failed'
        else:
            return 'No file uploaded'


@app.route('/description')
def description():
    data = {'descriptionPlayers': Parser.descriptionPlayers,
            'descriptionPolygons': Parser.descriptionPolygons,
            'Server': 'Server'}
    return jsonify(data)


@app.route('/description/player/<int:id>/coordinates')
def player_coordinates(id):
    try:
        data=dict()
        for i in Parser.Players:
            if int(id)==i.numPlayer:
                data.update([('numPlayer', i.numPlayer), ('timeGameCoordinates', i.timeGameCoordinates), ('coordinates', i.coordinates)])
                return jsonify(data)
        return 'No player'
    except Exception as e:
        print(e)
        return 'Error'


@app.route('/description/player/<int:id>/events')
def player_events(id):
    try:
        descriptionEvent = {0: 'No Event', 1: 'Player Event Min; Connect Player', 50: 'Player Event Max',
                            51: ' Role Player Event Min; cargo Action',
                            100: 'Role Player Event Max', 101: 'Object Control Event Min; create Object',
                            150: 'Object Control Event Max', 151: 'Method Control Event Min; create Method',
                            200: 'Method Control Event Max', 2: 'disconnect Player', 10: 'block Player',
                            11: 'unblock Player', 52: 'shoot Action', 60: 'cargo Loading', 61: 'cargo Unloading',
                            62: 'bonus Taking', 70: 'reload', 71: 'block Player', 98: 'create Role', 99: 'delete Role',
                            102: 'delete Object', 103: 'set Led', 152: 'delete Method'}
        data=dict()
        for i in Parser.Players:
            if int(id)==i.numPlayer:
                data.update([('numPlayer', i.numPlayer), ('timeGameEvents', i.timeGameEvent), ('event', i.event),
                             ('paramEvent', i.paramEvent), ('descriptionEvent', descriptionEvent)])
                return jsonify(data)
        return 'No player'
    except Exception as e:
        print(e)
        return 'Error'


@app.route('/description/player/<int:id>/RC')
def player_RC(id):
    try:
        data=dict()
        for i in Parser.Players:
            if int(id)==i.numPlayer:
                data.update([('numPlayer', i.numPlayer), ('timeGame', i.timeGameCoordinates), ('RC', i.RC)])
                return jsonify(data)
        return 'No player'
    except Exception as e:
        print(e)
        return 'Error'


@app.route('/description/player/<int:id>/yaw')
def player_yaw(id):
    try:
        data=dict()
        for i in Parser.Players:
            if int(id)==i.numPlayer:
                data.update([('numPlayer', i.numPlayer), ('timeGame', i.timeGameCoordinates), ('yaw', i.yaw)])
                return jsonify(data)
        return 'No player'
    except Exception as e:
        print(e)
        return 'Error'


@app.route('/description/polygon/<int:id>')
def polygon(id):
    try:
        descriptionEvent = {0: 'No Event', 1: ' Polygon Object Event Min; create Object', 50: 'Polygon Object Event Max',
                            51: 'Role Polygon Event Min; create Role', 100: 'Role Polygon Event Max', 2: 'delete Object', 3: 'setLed',
                            52: 'start Role', 53: 'delete Role', 54: 'block Player', 55: 'create Product',
                            56: 'get Product', 57: 'give Product'}
        data=dict()
        for i in Parser.Polygons:
            if int(id)==i.numPolygon:
                data.update([('numPolygon', i.numPolygon), ('timeGame', i.timeGame), ('event', i.event),
                             ('paramEvent', i.paramEvent), ('descriptionEvent', descriptionEvent)])
                return jsonify(data)
        return 'No polygon'
    except Exception as e:
        print(e)
        return 'Error'


@app.route('/description/server')
def server():
    try:
        descriptionEvent = {0: 'No Event', 1: 'Control Server Event Min; Waiting Game', 50: 'Control Server Event Max',
                            150: 'Service Server Event Min', 200: 'Service Server Event Max',
                            201: 'Error Server Event Min; create Game Error',
                            255: 'Error Server Event Max', 2: 'create Game', 3: 'start Game', 4: 'reset Game',
                            5: 'stop Game', 6: 'end Game', 202: 'create Log Directory Error'}
        data=dict()
        data.update([('event', Parser.server.event), ('timeGame', Parser.server.timeGame),
                       ('paramEvent', Parser.server.paramEvent), ('descriptionEvent', descriptionEvent)])
        return jsonify(data)
    except Exception as e:
        print(e)
        return 'Error'


if __name__ == '__main__':
    app.run(debug=False)

