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
 
	#packages
	sql = '''
            SELECT pb.trip_id, t.trip_start_date, t.trip_end_date, pb.customer_username,
                   (SELECT GROUP_CONCAT(name SEPARATOR ', ')
                    FROM trip_common
                    WHERE trip_trip_id = t.trip_id) AS items
            FROM package_booking pb
            INNER JOIN trip t ON pb.trip_id = t.trip_id
            WHERE pb.customer_username = %s
            '''
	cursor.execute(sql, (session['username'],))

	rows = cursor.fetchall()
            
	# Convert rows to a list of dictionaries
	package_bookings = []
	for row in rows:
		package_booking = {
			'trip_id': row[0],
			'trip_start_date': str(row[1]),
			'trip_end_date': str(row[2]),
			'customer_username': row[3],
			'itenary': row[4]
		}
		package_bookings.append(package_booking)
	print(package_bookings)
	return render_template('booking-history.html', package_bookings=package_bookings, items=activities, session=session, total_cost=total_cost)
