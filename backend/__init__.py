import http
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
    return id
    #flask.Response("", status=http.HTTPStatus.ACCEPTED)
    #return flask.Response("", status=http.HTTPStatus.BAD_REQUEST)

@app.route('/chat', methods = ['GET','POST'])
def chat():
    return app.send_static_file('chat.html')

@app.route('/message', methods = ['GET', 'POST'])
def message_get() -> str:
    return str(database.message_get_all())
   

@app.route('/message',methods = ['POST'])
def message_post():
    if not database.message_insert(flask.request.form['user_id'],flask.request.form['message']):
        pass

def run_backend():
    app.secret_key = "key"
    app.run()
