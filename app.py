from bottle import route, response, request, run, send_file
from bottle import mako_view as view
import simplejson as json
import edsger

@route('/evaluate', method="GET")
def evaluate():
	expression = request.GET["expression"]
	
	response.content_type = 'text/json'
	try:
		result = edsger.evaluate(expression)
		return json.dumps(result)
	except Exception, err:
		return json.dumps(err.__class__.__name__ + ": " + str(err))
	
@route('/')
@view('index')
def index():
	return {}
	
@route('/scripts/:filename')
def static_script(filename):
	send_file(filename, root="scripts")

run(reloader=True, host='localhost', port=8080)
