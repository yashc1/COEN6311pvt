

from flask import Flask, flash, render_template, request, redirect, session, url_for, Blueprint

from src.database import Database
activities_blueprint = Blueprint('activities_blueprint', __name__)
db = Database().db

def create_trip(no_error):

	# Query database when user is admin for admin panel
	if session['is_admin']:

		# Get user table information.
		cursor = db.cursor()
		cursor.execute("select * from user;")
		users = [dict(is_admin="Yes" if row[3] == 1 else "No", username=row[0], password=row[1], first_name=row[4], last_name=row[5], email=row[2], suspended="Yes" if row[7] == 1 else "No") for row in cursor.fetchall()]

		# Get attraction table information.
		attractions = get_attractions_data()

		if no_error:
			return render_template("home.html", session=session, users=users, attractions=attractions, no_trip="Here, you can start making your first trip!")
		else:
			return render_template("home.html", session=session, users=users, attractions=attractions, no_trip_error="You must first create a new trip!")

	# Not an admin
	if no_error:
		if 'current_trip_id' not in session or not session['current_trip_id']:
			return render_template("home.html", session=session, no_trip="Here, you can start making a new trip!")
		return render_template("home.html", session=session)
	else:
		return render_template("home.html", session=session, no_trip_error="You must first create a new trip!")



#####################################################################
#                        Activities                                 #
#####################################################################

def add_attraction_to_trip(attraction_name, activity_name, start_time, end_time, date, cost):
	return "insert into activity (activity_name, activity_start_time, activity_end_time, activity_date, attraction_name, username, trip_id, cost) values ('" + activity_name + "', '" + start_time + "', '" + end_time + "', '" + date + "', '" + attraction_name + "', '" + session['username'] + "', " + str(session['current_trip_id']) + ", " + str(cost) + ");"



def get_attractions_data():

	cursor = db.cursor()
	cursor.execute("select * from activities;")
	attractions = [dict(name=row[1], description=row[2], address=row[3],price=row[4]) for row in cursor.fetchall()]
	return attractions

# Shows all available attractions.
@activities_blueprint.route('/attractions')
def attractions():

	attractions = get_attractions_data()
	return render_template('attractions.html', items=attractions, session=session)

# Receive attraction data to turn into an activity
@activities_blueprint.route('/add-to-trip/<attraction_index>', methods=['POST'])
def add_to_trip(attraction_index):

	# TODO: Check if the attraction_name is on list of attractions
	print(session['current_trip_id'])
	if 'current_trip_id' not in session or not session['current_trip_id']:
		return create_trip(no_error=False)

	cursor = db.cursor()

	# Get attraction data
	cursor.execute("select * from activities;")
	attractions = [dict(name=row[1], description=row[2], address=row[3],price=row[4]) for row in cursor.fetchall()]
	attraction_name = attractions[int(attraction_index) - 1]['name']
	db.commit()

	return render_template('create_activity.html', session=session, attraction_name=attraction_name)

# Insert activity into database
@activities_blueprint.route('/create-activity', methods=['POST', 'GET'])
def create_activity():

	if 'current_trip_id' not in session or not session['current_trip_id']:
		return create_trip(no_error=False)

	# Get activity field data.
	attraction_name = request.form['attraction_name']
	activity_name = request.form['activity_name']
	start_time = request.form['start_time']
	end_time = request.form['end_time']
	date = request.form['date']
	cost = request.form['cost'][1:]

	# Add attraction to trip
	cursor = db.cursor()
	query = add_attraction_to_trip(attraction_name, activity_name, start_time, end_time, date, cost)
	cursor.execute(query)
	db.commit()

	success = attraction_name + " added to My Trip!"
	attractions = get_attractions_data()
	return render_template('attractions.html', items=attractions, session=session, success=success)

# Delete an attraction
@activities_blueprint.route('/delete-attraction/<attraction_index>')
def delete_attraction(attraction_index):

	# Get attraction_name
	cursor = db.cursor()
	cursor.execute("select attraction.attraction_name from attraction natural join address;")
	attraction_name = cursor.fetchall()[int(attraction_index) - 1][0]

	# Delete from database
	cursor.execute("delete from attraction where attraction_name='" + attraction_name + "';")
	db.commit()
	return redirect(url_for('home'))

