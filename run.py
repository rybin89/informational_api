from flask import Flask,jsonify,request
import locale
from app.Routes.AuthRoute import auth_bp

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
application = Flask(__name__)

application.register_blueprint(auth_bp)


if __name__ == "__main__":
    application.run(debug=True,port=5111)
