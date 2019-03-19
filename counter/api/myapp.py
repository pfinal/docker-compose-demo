from flask import Flask, request, jsonify, g
import redis

from demo.models import db

app = Flask(__name__)

app.config.from_object('demo.config')
db.init_app(app)


@app.route('/')
def home():
    return "counter api service"


@app.route('/version')
def version():
    return "0.0.1"


@app.route('/list')
def index():
    print('uid:{}'.format(g.uid))

    pool = redis.ConnectionPool(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])
    rd = redis.Redis(connection_pool=pool)

    results = rd.mget(['count:{}:A'.format(g.uid), 'count:{}:B'.format(g.uid), 'count:{}:C'.format(g.uid)])
    print(results)

    data = {
        'status': True,
        'data': [i.decode("utf-8") if i != None else "0" for i in results]
    }

    return jsonify(data)


@app.route('/incr')
def incr():
    print('uid:{}'.format(g.uid))

    pool = redis.ConnectionPool(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])
    rd = redis.Redis(connection_pool=pool)

    tag = request.args['tag']

    count = rd.incr('count:{}:{}'.format(g.uid, tag))

    data = {
        'status': True,
        'data': '{}'.format(count)
    }

    return jsonify(data)


@app.route('/reset')
def reset():
    pool = redis.ConnectionPool(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])

    rd = redis.Redis(connection_pool=pool)

    rd.delete('count:{}:A'.format(g.uid))
    rd.delete('count:{}:B'.format(g.uid))
    rd.delete('count:{}:C'.format(g.uid))

    data = {
        'status': True,
        'data': None
    }

    return jsonify(data)


@app.after_request
def after_filter(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PUT,'
    allow_headers = "Referer,Accept,Origin,User-Agent"
    response.headers['Access-Control-Allow-Headers'] = allow_headers

    return response


@app.route('/token', methods=["POST", "GET"])
def token():
    import hashlib
    import uuid
    from flask import jsonify, request
    from demo.models import User

    username = request.values.get('username')
    password = request.values.get('password')

    if not username or not password:
        return jsonify({'status': False, 'data': '用户名或密码无效'})

    hash = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()

    user = User.query.filter_by(username=username).first()
    if user == None or user.password != hash:
        return jsonify({'status': False, 'data': '用户名或密码无效'})

    token = str(uuid.uuid4().hex)
    print({"token": token, "uid": user.id})

    pool = redis.ConnectionPool(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])
    rd = redis.Redis(connection_pool=pool)
    rd.set('token:{}'.format(token), user.id, 60 * 60 * 24)  # 缓存1天

    return jsonify({'status': True, 'data': {'token': token}})


@app.route('/logout', methods=["POST", "GET"])
def logout():
    pool = redis.ConnectionPool(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])
    rd = redis.Redis(connection_pool=pool)

    token = request.args.get('token')
    rd.delete('token:{}'.format(token))

    return jsonify({'status': True, 'data': None})


@app.before_request
def before_filter():
    from flask import request, jsonify

    endpoint = request.endpoint

    print(endpoint)

    if endpoint in ['home', 'version', 'token']:
        return

    token = request.args.get('token')
    if token is None:
        return jsonify({'status': False, 'data': 'INVALID_TOKEN'})

    pool = redis.ConnectionPool(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'])
    rd = redis.Redis(connection_pool=pool)
    uid = rd.get('token:{}'.format(token))

    if (uid is None):
        return jsonify({'status': False, 'data': 'INVALID_TOKEN'})

    print('uid:{}'.format(uid.decode()))

    g.uid = uid.decode()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
