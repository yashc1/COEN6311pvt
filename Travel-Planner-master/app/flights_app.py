from src.flight import Flight
from flask import Flask, flash, render_template, request, redirect, session, url_for, Blueprint

from src.database import Database

from app.trip_app import create_trip
flight_blueprint = Blueprint('flight_blueprint', __name__)
#####################################################################
#                             Flights                               #
#####################################################################


db = Database().db

def get_flight_data():

	cursor = db.cursor()
	cursor.execute("select * from flights;")
	flights = [dict(flight_number=row[1], airline_name=row[2], departure_date=row[3],departure_time=row[4],departure_airport=row[5],arrival_airport=row[6],duration=row[7],price=row[8]) for row in cursor.fetchall()]
	return flights


# Shows all available attractions.
@flight_blueprint.route('/flights')
def view_flights():

	flights = get_flight_data()
	return render_template('flights.html', items=flights, session=session)

# Insert activity into database

@flight_blueprint.route('/flights-admin', methods=['GET'])
def add_flight():
	return render_template('flights-admin.html')

@flight_blueprint.route('/flight/<int:flight_id>')
def get_flight(flight_id):
    flight = Flight.get_flight_by_id(flight_id)
    
    if flight:
        return render_template('flights-admin.html', flight=flight)
    return "Flight not found."

@flight_blueprint.route('/flights-create', methods=['POST'])
def create_flight():
    
	if request.method == 'POST':
		airline_name = request.form['airline_name']
		flight_number = request.form['flight_number']
		departure_airport = request.form['departure_airport']
		departure_time = str(request.form['departure_time'])
		departure_date = str(request.form['departure_date'])
		arrival_airport = request.form['arrival_airport']
		price = request.form['price']
		duration = request.form['duration_flight']
		print(airline_name, flight_number, departure_airport,departure_date, departure_time, arrival_airport, duration, price)
		fl_ob = Flight(airline_name, flight_number, departure_airport,departure_date, departure_time, arrival_airport, duration, price)
		fl_ob.save()
		return redirect('/home')
	return render_template('flights-admin.html')


@flight_blueprint.route('/add-to-flight/<attraction_index>', methods=['POST'])
def add_to_flight(attraction_index):

	# TODO: Check if the attraction_name is on list of attractions
	print(session['current_trip_id'])
	if 'current_trip_id' not in session or not session['current_trip_id']:
		return create_trip(no_error=False)
	cursor = db.cursor()
	# Get attraction data
	cursor.execute("select * from flights;")
	db.commit()
	flights_selection = [dict(name=row[2], number=row[1],price=row[8]) for row in cursor.fetchall()]
	flight_name = flights_selection[int(attraction_index) - 1]['name']
	flight_number = flights_selection[int(attraction_index) - 1]['number']
	flight_price = flights_selection[int(attraction_index) - 1]['price']
	values = (flight_name, flight_price,flight_number,  session['username'], 0)
	query_trip_common = "INSERT INTO trip_common ( name ,price,number, username, is_booked) VALUES (%s, %s, %s, %s, %s)"
	cursor.execute(query_trip_common, values)
	db.commit()

	return render_template('trip.html', session=session, attraction_name=flight_name)

@flight_blueprint.route('/flight/edit/<int:flight_id>', methods=['GET', 'POST'])
def edit_flight(flight_id):
    flight = Flight.get_flight_by_id(flight_id)
    if flight:
        if request.method == 'POST':
            flight.name = request.form['name']
            flight.origin = request.form['origin']
            flight.destination = request.form['destination']
            flight.update()
            return redirect('/')
        return render_template('edit_flight.html', flight=flight)
    return "Flight not found."

@flight_blueprint.route('/flight/delete/<int:flight_id>')
def delete_flight(flight_id):
    flight = Flight.get_flight_by_id(flight_id)
    if flight:
        flight.delete()
        return redirect('/')
    return "Flight not found."