from config import *

class BookCategory(db.Model):
    __tablename__ = 'book_categories'
    book_category_id = db.Column(db.Integer, primary_key=True)
    book_category_name = db.Column(db.String(100), unique=True, nullable=False)
    book_category_status = db.Column(db.Integer, nullable=False) 