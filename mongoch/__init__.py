import http
import json
import html
import flask

import database


app = flask.Flask(__name__, static_url_path="")


@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")


@app.route("/user", methods=["POST"])
def user_reg():
    id = database.user.insert(flask.request.form["nickname"])
    id = html.escape(id)
    return flask.Response(response=id, status=http.HTTPStatus.OK)


@app.route("/user", methods=["GET"])
def user_info():
    user_id = flask.request.args.get("user_id")
    return database.user.get_info(user_id)


@app.route("/user", methods=["PATCH"])
def user_change_name():
    data = flask.request.get_json()
    user_id = data["user_id"]
    new_name = data["new_name"]
    if database.user.change_name(user_id, new_name):
        return flask.Response(response="", status=http.HTTPStatus.OK)
    else:
        return flask.Response(response="", status=http.HTTPStatus.BAD_REQUEST)


@app.route("/user", methods=["DELETE"])
def user_delete():
    data = flask.request.get_json()
    user_id = data["user_id"]
    if database.user.delete(user_id):
        return flask.Response(response="", status=http.HTTPStatus.OK)
    else:
        return flask.Response(response="", status=http.HTTPStatus.BAD_REQUEST)


@app.route("/chat", methods=["GET"])
def chat():
    return app.send_static_file("chat.html")


@app.route("/message", methods=["GET"])
def message_get() -> str:
    return json.dumps(database.message.get_all())


@app.route("/message", methods=["POST"])
def message_post():
    user_id = flask.request.form["user_id"]
    msg = flask.request.form["message"]
    msg = html.escape(msg)
    if database.message.insert(user_id, msg):
        return flask.Response(response="", status=http.HTTPStatus.OK)
    else:
        return flask.Response(response="", status=http.HTTPStatus.BAD_REQUEST)


@app.route("/message", methods=["PATCH"])
def message_update():
    data = flask.request.get_json()
    user_id = data["user_id"]
    msg_id = data["msg_id"]
    new_msg = data["new_msg"]
    if database.message.edit_one(user_id, msg_id, new_msg):
        return flask.Response(response="", status=http.HTTPStatus.OK)
    else:
        return flask.Response(response="", status=http.HTTPStatus.BAD_REQUEST)


@app.route("/message", methods=["DELETE"])
def message_delete():
    data = flask.request.get_json()
    user_id = data["user_id"]
    msg_id = data["msg_id"]
    if database.message.delete_one(user_id, msg_id):
        return flask.Response(response="", status=http.HTTPStatus.OK)
    else:
        return flask.Response(response="", status=http.HTTPStatus.BAD_REQUEST)


@app.route("/statistic", methods=["GET"])
def analysis():
    user_id = flask.request.args.get("user_id", "", type=str)
    if user_id == "":
        return flask.Response(response="", status=http.HTTPStatus.BAD_REQUEST)
    return database.message.get_all_statistics()


def run():
    app.secret_key = "key"
    app.run()
