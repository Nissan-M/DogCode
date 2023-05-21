from flask import Flask
from app.routes import register_routes


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
register_routes(app)


if __name__ == '__main__':
    app.run(debug=True)
