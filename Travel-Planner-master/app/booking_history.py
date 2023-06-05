from flask import Flask, flash, render_template, request, redirect, session, url_for, Blueprint
from src.database import Database
from app.activities_app import get_attractions_data

booking_blueprint = Blueprint('booking_blueprint', __name__)

#####################################################################
#                          SQL Queries                              #
#####################################################################
def get_trip_cost():
	return "select sum(price) from trip_common  where username=\"" + (session['username']) + "\"and is_booked = true;"

def get_all_activities_in_a_trip():
	# return "select activity_date, activity_name, cost, activity_start_time, activity_end_time, activity_id from activity natural join trip where username = '" + session['username'] + "' and is_booked = false;"
	return "select * from trip_common where username = '" + session['username'] + "' and is_booked = true;";
 

db = Database().db

#####################################################################
#                                TRIP                               #
#####################################################################

# Shows current trip itinerary.
@booking_blueprint.route('/booking-history')
def booking_trip():

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
	return render_template('booking-history.html', items=activities, session=session, total_cost=total_cost)
