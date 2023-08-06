from flask import Flask, jsonify
from flask_socketio import SocketIO, disconnect
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
from zou.app import config
from zou.app.stores import auth_tokens_store

from gevent import monkey
monkey.patch_all()


def get_redis_url():
    redis_host = config.KEY_VALUE_STORE["host"]
    redis_port = config.KEY_VALUE_STORE["port"]
    return "redis://%s:%s/2" % (redis_host, redis_port)


def create_app(redis_url):
    socketio = SocketIO(logger=True)

    app = Flask(__name__)
    jwt = JWTManager(app)
    app.config["SECRET_KEY"] = config.SECRET_KEY

    def configure_auth():
        @jwt.token_in_blacklist_loader
        def check_if_token_is_revoked(decrypted_token):
            return auth_tokens_store.is_revoked(decrypted_token)

    @app.route('/')
    def index():
        return jsonify({"name": "%s Event stream" % config.APP_NAME})

    @socketio.on("connect")
    def connected():
        app.logger.info("New websocket client connected")
        print("New websocket client connected")

    @socketio.on_error()
    def on_error(error):
        app.logger.error(error)

    configure_auth()
    socketio.init_app(app, message_queue=redis_url, async_mode="gevent")
    return (app, socketio)


redis_url = get_redis_url()
(app, socketio) = create_app(redis_url)

if __name__ == "main":
    socketio.run(app, debug=False, port=config["EVENT_STREAM_PORT"])
