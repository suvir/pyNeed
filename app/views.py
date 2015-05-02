from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
	#return "Hello, World!"
	user = {'nickname':'Suvir'}
	products = [{'cuisine':'italian','dish':'omelette du fromage'},
	{'cuisine':'thai','dish':'pad thai'},
	{'cuisine':'indian','dish':'butter chicken'}]
	return render_template('index.html',user=user,products = products )