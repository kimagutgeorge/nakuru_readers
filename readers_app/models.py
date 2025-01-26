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