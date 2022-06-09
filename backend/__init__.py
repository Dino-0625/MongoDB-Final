import http
import json
import html
import flask

import database


app = flask.Flask("mongoch", static_url_path='')


@app.route('/', methods=['GET', 'POST'])
def index():
    return app.send_static_file('index.html')


@app.route('/user', methods=['POST'])
def user_reg():
    id = database.user_add(flask.request.form['nickname'])
    id = html.escape(id)
    return flask.Response(response=id, status=http.HTTPStatus.OK)


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return app.send_static_file('chat.html')


@app.route('/message', methods=['GET'])
def message_get() -> str:
    return json.dumps(database.message_get_all())


@app.route('/message', methods=['POST'])
def message_post():
    user_id = flask.request.form['user_id']
    msg = flask.request.form['message']
    msg = html.escape(msg)
    database.message_insert(user_id, msg)
    return flask.Response(response="", status=http.HTTPStatus.OK)


def run():
    app.secret_key = "key"
    app.run()
