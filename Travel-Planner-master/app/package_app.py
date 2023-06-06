from flask import  render_template, request, redirect, session, url_for, Blueprint
from src.database import Database
from app.activities_app import get_attractions_data

package_blueprint = Blueprint('package_blueprint', __name__)

#####################################################################
#                          SQL Queries                              #
#####################################################################
def get_agent_trips():
	return """SELECT t.trip_id, t.trip_start_date, t.trip_end_date, t.username,
       (
           SELECT GROUP_CONCAT(tc.name SEPARATOR ', ')
           FROM trip_common tc
           WHERE tc.trip_trip_id = t.trip_id
           GROUP BY tc.trip_trip_id
       ) AS names
        FROM trip t
        JOIN user u ON t.username = u.username
        WHERE u.is_admin = 1 AND t.is_booked = 1;"""

 


#####################################################################
#                             Package                               #
#####################################################################

# Shows current trip itinerary.
@package_blueprint.route('/packages')
def booking_trip():

	# Get activity info for this trip
	db = Database().db
	cursor = db.cursor()
	query = get_agent_trips()
	cursor.execute(query)
	cursor.execute(query)
	agent_trips = [dict(id = row[0], trip_start_date=row[1], trip_end_date=row[2],username=row[3], names=row[4]) for row in cursor.fetchall()]
	return render_template('packages.html', items=agent_trips, session=session)
