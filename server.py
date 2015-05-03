import os
from app import app

port = os.getenv('VCAP_APP_PORT', 8000)

# For local usage
# app.run(debug=True)
# For bluemix
app.run(host='0.0.0.0', port=int(port))

