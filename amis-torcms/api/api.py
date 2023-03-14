from datetime import datetime
from functools import wraps

from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

account = {
    'username': 'admin',
    'password': 'admin123'
}
OK = 0
FAIL = 1

session = {}


def gen_response(status, msg, data):
    return jsonify({
        'status': status,
        'msg': msg,
        'data': data
    })


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        proto = request.cookies
        if request.cookies.get("1234"):
            return func(*args, **kwargs)
        return jsonify({
            "STATE": "INVILADE_TOKEN"
        })

    return decorated_view


@app.route('/api/hello')
def hello_world():
    return 'Hello World'


@app.route('/api/v1/login', methods=["POST"])
def login():
    body = request.json
    if body['username'] == account['username'] and body['password'] == account['password']:
        resp = make_response(gen_response(OK, '登录成功', {
            'username': body['username']
        }))
        now = datetime.now()
        resp.set_cookie("amisToken", datetime.strftime(now, "%Y-%m-%d %H:%M:%S"), max_age=3600)
        return resp
    else:
        return make_response(gen_response(FAIL, '登录失败', {
            'username': body['username']
        }))


class auth_middle:

    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, *args, **kwargs):
        a = request.cooki
        print('中间件的代码上')
        obj = self.wsgi_app(*args, **kwargs)
        print('中间件的代码下')

        return obj


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5555)
