import os
from app import app

# For bluemix
port = os.getenv('VCAP_APP_PORT', 8000)
app.run(host='0.0.0.0', port=int(port))

