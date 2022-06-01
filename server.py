from flask_app import app
from flask_app.controllers import users
from flask_app.controllers import events
import os
from dotenv import dotenv_values

app.secret_key = os.environ.get("SECRET_KEY")
if __name__ == "__main__":
    app.run(debug = True)