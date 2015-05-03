import os
from flask.ext.script import Manager, Server
from app import app

# For local normal usage
#app.run(debug=True)

# For local debugging usage
# manager = Manager(app)
# manager.add_command("runserver", Server(
#     use_debugger=True,
#     use_reloader=True,
#     host='0.0.0.0')
# )
#
# if __name__ == "__main__":
#     manager.run()

# For bluemix
port = os.getenv('VCAP_APP_PORT', 8000)
app.run(host='0.0.0.0', port=int(port))

