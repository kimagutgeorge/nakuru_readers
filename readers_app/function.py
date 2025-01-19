#imports
from models import *

@app.route('/add-category', methods=['POST'])
def addCategory():
    data = request.get_json()
    category_name = data.get('name')
    status = 0
    if category_name:
        # Create a new Category instance
        new_category = BookCategory(book_category_name=category_name, book_category_status = status)
        
        # Add the new category to the session
        db.session.add(new_category)
        
        # Commit the session to save it in the database
        db.session.commit()

        return {"message": "1"}, 200 #save
    else:
        return {"message": "2"}, 400 #not saved

    