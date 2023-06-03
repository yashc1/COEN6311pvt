
from src.hotel import Hotel
from flask import Flask, flash, render_template, request, redirect, session, url_for, Blueprint

from src.database import Database

hotels_blueprint = Blueprint('hotels_blueprint', __name__)
#####################################################################
#                             Hotels                                #
#####################################################################

db = Database().db

def get_hotel_data():

	cursor = db.cursor()
	cursor.execute("select * from hotels;")
	hotels = [dict(hotel_number=row[1], hotel_name=row[2], address=row[3],city=row[4],country=row[5],hotel_rating=row[6],price=row[7]) for row in cursor.fetchall()]
	return hotels

# Shows all available attractions.
@hotels_blueprint.route('/hotels')
def view_hotels():

	hotels = get_hotel_data()
	return render_template('hotels.html', items=hotels, session=session)

# Receive attraction data to turn into an activity
@hotels_blueprint.route('/add-to-hotels/<attraction_index>', methods=['POST'])
def add_to_hotels(attraction_index):

	# TODO: Check if the attraction_name is on list of attractions
	print(session['current_trip_id'])
	if 'current_trip_id' not in session or not session['current_trip_id']:
		# return create_trip(no_error=False)
		print("hello")

	cursor = db.cursor()

	# Get attraction data
	cursor.execute("select * from activities;")
	attractions = [dict(name=row[1], description=row[2], address=row[3],price=row[4]) for row in cursor.fetchall()]
	attraction_name = attractions[int(attraction_index) - 1]['name']
	db.commit()

	return render_template('create_activity.html', session=session, attraction_name=attraction_name)
@hotels_blueprint.route('/hotels-admin', methods=['GET'])
def add_hotels():
	return render_template('hotels.html')



@hotels_blueprint.route('/hotels-create', methods=['POST'])
def create_hotel():
    
	if request.method == 'POST':
		hotel_number = request.form['hotel_number']
		hotel_name = request.form['hotel_name']
		hote_address = request.form['hotel_address']
		city = str(request.form['city'])
		country = str(request.form['country'])
		hotel_rating = request.form['hotel_rating']
		price = request.form['price']
		print(hotel_name, hotel_number, hote_address,city, country, hotel_rating, price)
		hl_ob = Hotel(hotel_number, hotel_name, hote_address,city, country, hotel_rating, price)
		hl_ob.save()
		return redirect('/home')
	return render_template('hotels-admin.html')