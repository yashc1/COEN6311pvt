from flask import Flask, flash, render_template, request, redirect, session, url_for, Blueprint
from src.database import Database
from app.activities_app import get_attractions_data

trip_blueprint = Blueprint('trip_blueprint', __name__)

#####################################################################
#                          SQL Queries                              #
#####################################################################
def view_completed_attractions_query():
	 return "select activity_date, attraction.attraction_name, description from activity natural join attraction where activity.username = '" + session['username'] + "' and ((activity_date = CURDATE() and activity_end_time <= CURTIME()) or activity_date < CURDATE());"

def get_trip_cost():
	return "select sum(price) from trip_common  where username=\"" + (session['username']) + "\"and is_booked = false;"

def get_all_activities_in_a_trip():
	# return "select activity_date, activity_name, cost, activity_start_time, activity_end_time, activity_id from activity natural join trip where username = '" + session['username'] + "' and is_booked = false;"
	return "select * from trip_common where username = '" + session['username'] + "' and is_booked = false;";


def get_current_trip_id():
	return "select trip_id from trip natural join user where trip.is_booked=false and user.username='" + session['username'] + "';"

def add_attraction_to_trip(attraction_name, activity_name, start_time, end_time, date, cost):
	return "insert into activity (activity_name, activity_start_time, activity_end_time, activity_date, attraction_name, username, trip_id, cost) values ('" + activity_name + "', '" + start_time + "', '" + end_time + "', '" + date + "', '" + attraction_name + "', '" + session['username'] + "', " + str(session['current_trip_id']) + ", " + str(cost) + ");"


db = Database().db

#####################################################################
#                                TRIP                               #
#####################################################################

# Shows current trip itinerary.
@trip_blueprint.route('/trip')
def trip():

	# Create a trip if none exists
	if 'current_trip_id' not in session or not session['current_trip_id']:
		print("No trip exists") 
		return create_trip(no_error=False)

	# Get activity info for this trip
	db = Database().db
	cursor = db.cursor()
	query = get_all_activities_in_a_trip()
	cursor.execute(query)
	activities = [dict(id = row[0], name=row[1], number=row[2],price=row[3]) for row in cursor.fetchall()] # TODO: Correctly map activity info.
	# Calculate total cost of trip
	query = get_trip_cost()
	cursor.execute(query)
	amount = cursor.fetchall()[0][0]
	# amount = 0
	total_cost = str(amount)
	return render_template('trip.html', items=activities, session=session, total_cost=total_cost)

@trip_blueprint.route('/complete')
def complete():

	# Create a trip if none exists
	if 'current_trip_id' not in session or not session['current_trip_id']:
		return create_trip(no_error=False)

	# Pay if total cost > 0, else update trip_id record to "booked"
	cursor = db.cursor()
	query = get_trip_cost()
	cursor.execute(query)
	total_cost = cursor.fetchall()[0][0]

	if total_cost is None:
		total_cost = 0

	if total_cost > 0:

		# Check if a credit card is on file for this user.
		query = "select creditcard_id from creditcard, user where user.username='" + session['username'] + "' and user.username=creditcard.username;"
		cursor.execute(query)
		num_cards = len(cursor.fetchall())

		if num_cards == 0:
			# No credit card on file
			return render_template('payment.html', session=session, total_cost=total_cost)
		else:
			# Already have a credit card; they're fine.
			return redirect(url_for('trip_blueprint.trip_booked'))
	else:
		return redirect(url_for('trip_blueprint.trip_booked'))

@trip_blueprint.route('/pay', methods=['POST'])
def pay():

	# Create a trip if none exists
	if 'current_trip_id' not in session or not session['current_trip_id']:
		return create_trip(no_error=False)

	card_number="".join(request.form['card_number'].split('-'))
	first_name=request.form['first_name']
	last_name=request.form['last_name']
	exp_month=request.form['expiration_month']
	exp_year=request.form['expiration_year']

	# Get Address ID
	cursor = db.cursor()
	cursor.execute("select address_id from user where username='" + session['username'] + "';")
	address_id = cursor.fetchall()[0][0]

	# Insert credit card information
	query = "insert into creditcard (card_number, username, first_name, last_name, exp_month, exp_year, address_id) values ('" + card_number + "', '" + session['username'] + "', '" + first_name + "', '" + last_name + "', " + str(exp_month) + ", " + str(exp_year) + ", " + str(address_id) + ");"

	return redirect(url_for('trip_blueprint.trip_booked'))

# Render home page once a trip has been successfully booked.
# TODO: Return a Trip ID so that a user can view their previous trips
@trip_blueprint.route('/trip-booked')
def trip_booked():

	# Create a trip if none exists
	if 'current_trip_id' not in session or not session['current_trip_id']:
		return create_trip(no_error=False)

	cursor = db.cursor()
	cursor.execute("update trip_common set is_booked=1 where username=\"" + str(session['username']) + "\";")
	db.commit()

	session['current_trip_id'] = False
	trip_booked_message = "Congratulations! You're all set!"

	# Query database when user is admin for admin panel
	if session['is_admin']:

		# Get user table information.
		cursor = db.cursor()
		cursor.execute("select * from user;")
		users = [dict(is_admin="Yes" if row[3] == 1 else "No", username=row[0], password=row[1], first_name=row[4], last_name=row[5], email=row[2], suspended="Yes" if row[7] == 1 else "No") for row in cursor.fetchall()]

		# Get attraction table information.
		cursor.execute("select * from attraction natural join address;")
		attractions = [dict(name=row[1], description=row[2], nearest_transport=row[3], 
			address=(str(row[4]) if row[4] is not None else "") + " " + (row[5] if row[5] is not None else "") + " " + (row[6] if row[6] is not None else "") + ", " + (row[7] if row[7] is not None else "") + " " + (row[8] if row[8] is not None else "") + " " + (row[9] if row[9] is not None else "")) for row in cursor.fetchall()]

		return render_template("home.html", session=session, users=users, attractions=attractions, trip_booked_message=trip_booked_message)

	return render_template('home.html', session=session, trip_booked_message=trip_booked_message)

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

# Create a new current trip id for the user
@trip_blueprint.route('/new-trip', methods=['POST'])
def new_trip():

	start_date = request.form['start_date']
	end_date = request.form['end_date']

	cursor = db.cursor()
	query = "insert into trip (is_booked, trip_start_date, trip_end_date, creditcard_id, username) values (0, '" + start_date + "', '" + end_date + "', 1, '" + session['username'] + "');"
	cursor.execute(query)
	db.commit()

	# Set current trip id for this user.
	query = get_current_trip_id()
	cursor.execute(query)
	session['current_trip_id'] = cursor.fetchall()[0][0]
	return redirect(url_for('trip_blueprint.trip'))

# Remove an activity from a trip
@trip_blueprint.route('/remove-from-trip/<activity_id>')
def remove_from_trip(activity_id):

	# Find out which activity it is from index.
	cursor = db.cursor()
	cursor.execute("delete from trip_common where trip_id=" + activity_id + ";")
	db.commit()

	return redirect(url_for('trip_blueprint.trip'))