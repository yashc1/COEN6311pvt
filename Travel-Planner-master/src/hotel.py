from src.database import Database
class Hotel:
    def __init__(self, hotel_number, name, address, city, country, star_rating,price):
        self.hotel_number = hotel_number
        self.name = name
        self.address = address
        self.city = city
        self.country = country
        self.star_rating = star_rating
        self.price = price
        self.db = Database().get_db()
        self.cursor = self.db.cursor()

    @staticmethod
    def get_all_hotels(cursor):
        query = "SELECT * FROM hotels"
        cursor.execute(query)
        result = cursor.fetchall()
        hotels = []
        for hotel in result:
            hotels.append(Hotel(*hotel, cursor=cursor, db=None))
        return hotels

    @staticmethod
    def get_hotel_by_hotel_number(hotel_number, cursor):
        query = "SELECT * FROM hotels WHERE hotel_number = %s"
        cursor.execute(query, (hotel_number,))
        result = cursor.fetchone()
        if result:
            return Hotel(*result, cursor=cursor, db=None)
        return None

    def save(self):
        query = "INSERT INTO hotels (hotel_number, hotel_name, hotel_address, city, country, hotel_rating, price) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (self.hotel_number, self.name, self.address, self.city, self.country, self.star_rating,
                  self.price)
        self.cursor.execute(query, values)
        self.db.commit()

    def update(self):
        query = "UPDATE hotels SET name = %s, address = %s, city = %s, country = %s, star_rating = %s, " \
                "amenities = %s WHERE hotel_number = %s"
        values = (self.name, self.address, self.city, self.country, self.star_rating, self.amenities,
                  self.hotel_number)
        self.cursor.execute(query, values)
        self.db.commit()

    def delete(self):
        query = "DELETE FROM hotels WHERE hotel_number = %s"
        self.cursor.execute(query, (self.hotel_number,))
        self.db.commit()
