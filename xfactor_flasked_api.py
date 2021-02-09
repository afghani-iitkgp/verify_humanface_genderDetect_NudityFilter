"""
Imports all necessary packages
"""

# Importing App level modules
from flask import Flask
import flask_compress
from flask_cors import CORS


from Scripts.xfactor_main import x_factor_app_main
from Scripts.Utility import utils

# Declaring App:
flasked_app = Flask(__name__)

# Compressing all response
flask_compress.Compress(flasked_app)

# Connecting all services
flasked_app.register_blueprint(x_factor_app_main)

CORS(flasked_app, resources={r"/*": {"origins": "*"}})


if __name__ == "__main__":
    flasked_app.run(host=utils.configuration["settings"]["ip"], port=utils.configuration["settings"]["port"], debug=True, threaded=True, use_reloader=False)


