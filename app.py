from flask import Flask
from extensions.limiter import limiter
from routes.main import main
# import cProfile
# import atexit

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB

limiter.init_app(app)
app.register_blueprint(main)

# profiler = cProfile.Profile()
# profiler.enable()

# def save_profile():
#     profiler.disable()
#     profiler.dump_stats("flask_profile.prof")
#     print("Profile saved to flask_profile.prof")

# atexit.register(save_profile)

if __name__ == "__main__":
    app.run(debug=False)
