from flask_app import app
from flask_app.controllers import usersController, uiController, activitiesController



if __name__ == "__main__":
    app.run(debug=True)

