import http
import json
import database
import flask
app = flask.Flask(__name__, static_url_path='')

@app.route('/', methods = ['GET', 'POST'])
def index():
    return app.send_static_file('index.html')

@app.route('/user', methods = ['POST'])
def reg():
    # if flask.request.method == 'POST':
    id = database.user_add(flask.request.form['nickname'])
    return flask.Response(response=id, status=http.HTTPStatus.OK)
    #flask.Response("", status=http.HTTPStatus.ACCEPTED)
    #return flask.Response("", status=http.HTTPStatus.BAD_REQUEST)

@app.route('/chat', methods = ['GET','POST'])
def chat():
    return app.send_static_file('chat.html')

@app.route('/message', methods = ['GET'])
def message_get() -> str:
    print(database.message_get_all())
    return json.dumps(database.message_get_all())

@app.route('/message',methods = ['POST'])
def message_post():
    database.message_insert(flask.request.form['user_id'],flask.request.form['message'])
    return flask.Response("", http.HTTPStatus.OK)

def run_backend():
    app.secret_key = "key"
    app.run()
