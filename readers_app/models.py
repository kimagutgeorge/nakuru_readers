from config import *

# book genres
class BookCategory(db.Model):
    __tablename__ = 'book_categories'
    book_category_id = db.Column(db.Integer, primary_key=True)
    book_category_name = db.Column(db.String(100), unique=True, nullable=False)
    book_category_status = db.Column(db.Integer, nullable=False)

# book genres
class BookCollection(db.Model):
    __tablename__ = 'book_collections'
    book_collection_id = db.Column(db.Integer, primary_key=True)
    book_collection_name = db.Column(db.String(100), unique=True, nullable=False)
    book_collection_status = db.Column(db.Integer, nullable=False) 

# book prduct details
class BookProduct(db.Model):
    __tablename__ = 'book_products'
    book_id = db.Column(db.Integer, primary_key = True)
    book_genre = db.Column(db.Integer, nullable = False)
    book_name = db.Column(db.String(120), unique=True, nullable = False)
    book_image = db.Column(db.Text, nullable = False)
    book_collection = db.Column(db.Integer, nullable = True)
    book_selling_price = db.Column(db.Integer, nullable = False)
    book_buying_price = db.Column(db.Integer, nullable = False)
    book_quantity = db.Column(db.Integer, nullable = False)
    book_balance = db.Column(db.Integer, nullable = False)
    book_discount = db.Column(db.Integer, nullable = False)
    book_description = db.Column(db.Text, nullable = False)

# users
class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    user_first_name = db.Column(db.String(40), nullable = False)
    user_last_name = db.Column(db.String(40), nullable = False)
    user_phone = db.Column(db.Integer, nullable = False)
    user_email = db.Column(db.String(80), nullable = False)
    user_registration_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_is_verified = db.Column(db.Integer, default="1", nullable=False)
    user_is_active = db.Column(db.Integer, default="1", nullable=True)
    user_last_login = db.Column(db.DateTime, nullable=True)
    user_preferred_genres = db.Column(db.JSON, nullable = True)
    user_last_active = db.Column(db.DateTime, nullable=True)
    user_total_books_read = db.Column(db.Integer, default=0)
    user_currently_reading = db.Column(db.Integer, nullable=True)
    user_wishlist = db.Column(db.JSON, nullable=True)
    user_profile_picture = db.Column(db.String(200), nullable=True)
    user_bio = db.Column(db.Text, nullable=True)
    user_location = db.Column(db.String(100), nullable=True)
    user_role = db.Column(db.String(20), default="1", nullable=False)
    user_unread_notifications = db.Column(db.Integer, default=0)
    user_average_rating = db.Column(db.Float, default=0.0)