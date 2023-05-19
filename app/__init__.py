from flask import Flask
from .routes import bp


app = Flask(__name__, template_folder='templates')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.register_blueprint(bp)


if __name__ == '__main__':
    app.run()
