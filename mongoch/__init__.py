import http
import json
import html
import flask

import database


app = flask.Flask(__name__, static_url_path='')


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')


@app.route('/user', methods=['POST'])
def user_reg():
    id = database.user.insert(flask.request.form['nickname'])
    id = html.escape(id)
    return flask.Response(response=id, status=http.HTTPStatus.OK)


@app.route('/user', methods=['GET'])
def user_info():
    user_id = flask.request.args.get("user_id")
    return database.user.get_info(user_id)


@app.route('/chat', methods=['GET'])
def chat():
    return app.send_static_file('chat.html')


@app.route('/message', methods=['GET'])
def message_get() -> str:
    return json.dumps(database.message.get_all())


@app.route('/message', methods=['POST'])
def message_post():
    user_id = flask.request.form['user_id']
    msg = flask.request.form['message']
    msg = html.escape(msg)
    database.message.insert(user_id, msg)
    return flask.Response(response="", status=http.HTTPStatus.OK)


@app.route('/analysis', methods=['GET'])
def analysis():
    user_id = flask.request.args.get("user_id", "", type=str)
    if user_id == "":
        return flask.Response(response="", status=http.HTTPStatus.BAD_REQUEST)
    return {
        "total_msg_count": database.message.get_count_of_everyone(),
        "total_char_count": database.message.get_char_count_of_everyone(),
        "avg_msg_len": database.message.get_avg_msg_len_of_everyone(),
    }


def run():
    app.secret_key = "key"
    app.run()
