from flask import Flask,render_template,request,escape,session,make_response
import googlemaps
from datetime import datetime


app = Flask(__name__)
app.secret_key='shubham'

@app.route('/')
@app.route('/shubham_maps',methods=['POST','GET'])
def Gmaps():
#	if request.form['submit'] == 'Back to Main Menu':
	return render_template('Gmaps.html',the_title='DISTANCE AND TIME CALCULATOR,POWERED BY GOOGLEMAPS')

@app.route('/finddist',methods=['POST','GET'])
def find():
	return render_template('finddist.html')


def finddist():
	print("Inside finddist")
	print(request)
	source = request.form['source']
	session['my_source']=source
	destination = request.form['destination']
	session['my_dest']=destination
	try:
		gmaps = googlemaps.Client(key="AIzaSyAItPICLADV5q3nVp7g_cIq1RU0NHEeEZw")
		now = datetime.now()
		dir_result = gmaps.directions(origin=source,destination=destination,mode="driving",departure_time=now)
#		print(dir_result)
		for map1 in dir_result:
			overall_stats = map1['legs']
			for dimensions in overall_stats:
				distance = dimensions['distance']
				duration = dimensions['duration']
				return [distance['text'],duration['text']]
	except:
		return 0

@app.route('/result',methods=['POST','GET'])
def result():
	res = finddist()
	if res == 0:
		return render_template('error.html',the_title="Error ! Please enter correct location")
	elif res[0]==None:
		return render_template('error.html',the_title="Error ! Please enter correct location")
	elif res[1] == None:
		return render_template('error.html',the_title="Error ! Please enter correct location")
	my_source = session['my_source']
	my_dest = session['my_dest']
	return render_template('result.html',the_title='Search Results',the_source=my_source,the_dest=my_dest,the_dist=res[0],the_time=res[1])

	
	
app.run(debug=True)