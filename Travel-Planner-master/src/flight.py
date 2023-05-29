

class Flight:
    def __init__(self, flight_number, airline, departure_airport, departure_datetime, arrival_airport, duration, db, cursor):
        self.flight_number = flight_number
        self.airline = airline
        self.departure_airport = departure_airport
        self.departure_datetime = departure_datetime
        self.arrival_airport = arrival_airport
        self.duration = duration
        self.db = db
        self.cursor = cursor

    def get_all_flights(self):
        query = "SELECT * FROM flights"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        flights = []
        for flight in result:
            flights.append(Flight(flight[0], flight[1], flight[2], flight[3], flight[4], flight[5]))
        return flights

    def get_flight_by_flight_number(self, flight_number):
        query = "SELECT * FROM flights WHERE flight_number = %s"
        self.cursor.execute(query, (flight_number,))
        result = self.cursor.fetchone()
        if result:
            return Flight(result[0], result[1], result[2], result[3], result[4], result[5])
        return None

    def save(self):
        query = "INSERT INTO flights (flight_number, airline, departure_airport, departure_datetime, " \
                "arrival_airport, duration) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (self.flight_number, self.airline, self.departure_airport, self.departure_datetime,
                  self.arrival_airport, self.duration)
        self.cursor.execute(query, values)
        self.db.commit()

    def update(self):
        query = "UPDATE flights SET airline = %s, departure_airport = %s, " \
                "departure_datetime = %s, arrival_airport = %s, duration = %s WHERE flight_number = %s"
        values = (self.airline, self.departure_airport, self.departure_datetime,
                  self.arrival_airport, self.duration, self.flight_number)
        self.cursor.execute(query, values)
        self.db.commit()

    def delete(self):
        query = "DELETE FROM flights WHERE flight_number = %s"
        self.cursor.execute(query, (self.flight_number,))
        self.db.commit()
