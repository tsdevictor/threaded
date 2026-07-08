from flask import Flask
from extensions.limiter import limiter
from routes.main import main

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB

limiter.init_app(app)
app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=False)
