from models import *

@app.route('/add-category', methods=['POST'])
def addCategory():
    data = request.get_json()
    category_name = data.get('name')
    status = 1  # Active status

    if category_name:
        # Check if the category already exists
        existing_category = BookCategory.query.filter_by(book_category_name=category_name).first()
        if existing_category:
            return {"message": "3"}, 201  # Conflict status code

        # Create a new Category instance
        new_category = BookCategory(book_category_name=category_name, book_category_status=status)
        
        # Add the new category to the session
        db.session.add(new_category)
        
        # Commit the session to save it in the database
        db.session.commit()

        return {"message": "1"}, 201  # Created status code
    else:
        return {"message": "2"}, 201  # Bad request

# fetch categories
@app.route('/get-categories', methods=['GET'])
def getCategories():
    categories = BookCategory.query.order_by(desc(BookCategory.book_category_id)).all()  # Fetch all categories from the database
    result = [{'id': category.book_category_id, 'name': category.book_category_name, 'status': category.book_category_status } for category in categories]
    return jsonify(result), 201

# edit category
@app.route('/save-category', methods=['POST'])
def editCategories():
    data = request.get_json()
    cat_id = data.get('id')
    cat_name = data.get('name')

    # Fetch the category by its ID
    category = BookCategory.query.get(cat_id)  
    if category:
         # Update the name
        category.book_category_name = cat_name 
         # Commit the changes
        db.session.commit() 
        return {"message": "1"}, 200
    else:
        return {"message": "2"}, 200

# change status category
@app.route('/status-category', methods=['POST'])
def editStatusCategory():
    data = request.get_json()
    cat_id = data.get('cat_id')
    cat_status = data.get('cat_status')

    # Fetch the category by its ID
    category = BookCategory.query.get(cat_id)  
    if category:
         # Update the status
        category.book_category_status = cat_status 
         # Commit the changes
        db.session.commit() 
        return {"message": "1"}, 200
    else:
        return {"message": "2"}, 200

#delete category    
@app.route('/del-category', methods = ['POST'])
def deleteCategory():
    data = request.get_json()
    cat_id = data.get('id')

    # Fetch the category by its ID
    category = BookCategory.query.get(cat_id)  
    if category:
        # If the category exists, delete it
        db.session.delete(category)
        db.session.commit() 
        return {"message": "1"}, 200
    else:
        return {"message": "2"}, 200

# add book
@app.route('/add-book', methods = ['POST'])
def addBook():
    description = request.form.get('description')
    genre = request.form.get('genre')
    bookName = request.form.get('bookName')
    productImage = request.files['productImage']
    collection = request.form.get('collection')
    sellingPrice = request.form.get('sellingPrice')
    buyingPrice = request.form.get('buyingPrice')
    quantity = request.form.get('quantity')
    discount = request.form.get('discount')

    if not discount:
        discount = '0'
    
    if not collection:
        collection = '1'

    similar_book = db.session.query(BookProduct).filter( BookProduct.book_name == bookName).scalar()

    if similar_book:
        return {"message": "3"}, 200  # Event already exists
    
    else:
        try:
            # Secure the filename and split extension
            original_filename = secure_filename(productImage.filename)
            name, ext = os.path.splitext(original_filename)
            
            # Convert extension to lowercase
            ext = ext.lower()

            # Validate the extension
            if ext.lstrip(".") not in ALLOWED_EXTENSIONS:
                return {"message": "4"}, 200 # invalid extension

            # Create the final filename
            filename = f"{name}{ext}"

            # Open the image
            img = Image.open(productImage)

            # Convert RGBA to RGB if necessary
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Define target size (e.g., 1200x800 for blog banners)
            target_size = (800, 800)
            img_resized = img.resize(target_size, Image.Resampling.LANCZOS)

            # Ensure the upload folder exists
            os.makedirs(app.config['BOOKS_FOLDER'], exist_ok=True)

            # Save the resized image to the upload folder
            file_path = os.path.join(app.config['BOOKS_FOLDER'], filename)
            img_resized.save(file_path, "JPEG" if ext in {".jpg", ".jpeg"} else ext.lstrip("."))

            # Save blog details to the database
            new_book = BookProduct(
                book_genre = genre,
                book_name = bookName,
                book_image = filename,
                book_collection = collection,
                book_selling_price = sellingPrice,
                book_buying_price = buyingPrice,
                book_quantity = quantity,
                book_balance = quantity,
                book_discount = discount,
                book_description = description
            )

            if new_book:
                db.session.add(new_book)
                db.session.commit()
                return {"message": "1"}, 200  # book saved successfully
            else:
                return {"message": "2"}, 100  # Error saving the book

        except Exception as e:
            print(e)
            return {"message": "3"}, 200 # error processing image

# get products
@app.route('/get-products', methods = ['GET'])
def getProducts():
    products = BookProduct.query.order_by(desc(BookProduct.book_id)).all()  # Fetch all products from the database
    # Build the result with image URLs
    result = []
    for book in products:
        image_url = url_for('static', filename=f'uploads/products/{book.book_image}', _external=True)
        result.append({
            'id': book.book_id,
            'name': book.book_name,
            'price': book.book_selling_price,
            'balance': book.book_balance,
            'image': image_url
        })
    
    return jsonify(result), 201

# view single product
@app.route('/get-product', methods = ['POST'])
def viewProduct():
    data = request.get_json()
    id = data.get("id")
    
    products = db.session.query(BookProduct, BookCategory, BookCollection).join(BookCategory, BookProduct.book_genre == BookCategory.book_category_id).join(BookCollection, BookProduct.book_collection == BookCollection.book_collection_id).filter(BookProduct.book_id == id)

    # Build the result with image URLs
    result = []
    for book, category, collection in products:
        image_url = url_for('static', filename=f'uploads/products/{book.book_image}', _external=True)
        result.append({
            'id': book.book_id,
            'name': book.book_name,
            'price': book.book_selling_price,
            'b_price':book.book_buying_price,
            'balance': book.book_balance,
            'discount': book.book_discount,
            'genre': category.book_category_name,
            'genre_id': book.book_genre,
            'collection': collection.book_collection_name,
            'collection_id': book.book_collection,
            'image': image_url,
            'description': book.book_description
        })
    
    return jsonify(result), 201

# add collection
@app.route('/add-collection', methods=['POST'])
def addCollection():
    data = request.get_json()
    collection_name = data.get('name')
    status = 1  # Active status

    if collection_name:
        # Check if the category already exists
        existing_collection = BookCollection.query.filter_by(book_collection_name=collection_name).first()
        if existing_collection:
            return {"message": "3"}, 201  # Conflict status code

        # Create a new Category instance
        new_collection = BookCollection(book_collection_name=collection_name, book_collection_status=status)
        
        # Add the new category to the session
        db.session.add(new_collection)
        
        # Commit the session to save it in the database
        db.session.commit()

        return {"message": "1"}, 201  # Created status code
    else:
        return {"message": "2"}, 201  # Bad request
    
# fetch collections
@app.route('/get-collections', methods=['GET'])
def getCollections():
    collections = BookCollection.query.order_by(desc(BookCollection.book_collection_id)).all()  # Fetch all collections from the database
    result = [{'id': collection.book_collection_id, 'name': collection.book_collection_name, 'status': collection.book_collection_status } for collection in collections]
    return jsonify(result), 201

# edit collection
@app.route('/save-collection', methods=['POST'])
def editCollection():
    data = request.get_json()
    collection_id = data.get('id')
    collection_name = data.get('name')

    # Fetch the collection by its ID
    collection = BookCollection.query.get(collection_id)  
    if collection:
         # Update the name
        collection.book_collection_name = collection_name 
         # Commit the changes
        db.session.commit() 
        return {"message": "1"}, 200
    else:
        return {"message": "2"}, 200
    
#delete collection    
@app.route('/del-collection', methods = ['POST'])
def deleteCollection():
    data = request.get_json()
    cat_id = data.get('id')

    # Fetch the category by its ID
    collection = BookCollection.query.get(cat_id)  
    if collection:
        # If the collection exists, delete it
        db.session.delete(collection)
        db.session.commit() 
        return {"message": "1"}, 200
    else:
        return {"message": "2"}, 200

# change status collection
@app.route('/status-collection', methods=['POST'])
def editStatusCollection():
    data = request.get_json()
    collection_id = data.get('collection_id')
    collection_status = data.get('collection_status')

    # Fetch the category by its ID
    collection = BookCollection.query.get(collection_id)  
    if collection:
         # Update the status
        collection.book_collection_status = collection_status 
         # Commit the changes
        db.session.commit() 
        return {"message": "1"}, 200
    else:
        return {"message": "2"}, 200

# Edit product
@app.route('/edit-book', methods=['POST'])
def editBook():
    description = request.form.get("description")
    genre = request.form.get("genre")
    bookName = request.form.get("bookName")
    collection = request.form.get("collection")
    sellingPrice = request.form.get("sellingPrice")
    buyingPrice = request.form.get("buyingPrice")
    quantity = request.form.get("quantity")
    discount = request.form.get("discount")
    product_id = request.form.get("id")

    try:
        # Start a transaction
        with db.session.begin():
            # Fetch the book with row-level locking
            product = db.session.execute(
                select(BookProduct)
                .where(BookProduct.book_id == product_id)
                .with_for_update()
            ).scalar_one()

            if product:
                # Update the product details
                product.book_genre = genre
                product.book_name = bookName
                product.book_collection = collection
                product.book_selling_price = sellingPrice
                product.book_buying_price = buyingPrice
                product.book_quantity = quantity
                product.book_balance = quantity
                product.book_discount = discount
                product.book_description = description

                # Commit the changes (implicitly done by the context manager)
                return {"message": "1"}, 200
            else:
                return {"message": "2"}, 200
    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        return {"message": f"An error occurred: {str(e)}"}, 500

# delete book
@app.route('/del-book', methods=['POST'])
def delBook():
    data = request.get_json()
    book_id = data.get('id')

    # Query the `event_banner` column for the given `event_id`
    book_banner = db.session.query(BookProduct).with_entities(BookProduct.book_image).filter_by(book_id=book_id).first()

    # Access the result
    if book_banner:
        book_banner_value = book_banner[0]  # Get the `event_banner` value from the tuple
        folder_path = app.config['BOOKS_FOLDER']
        file_path = os.path.join(folder_path, book_banner_value)
        os.remove(file_path)

        # delete event details from db
        book = BookProduct.query.get(book_id)  
        if book:
            # If the category exists, delete it
            db.session.delete(book)
            db.session.commit() 
            return {"message": "1"}, 200
    else:
        return {"message": "2"}, 200 # error deleting

# get users
@app.route('/get-users', methods=['GET'])
def getUsers():
    # Fetch all users and format the result
    users = Users.query.order_by(desc(Users.user_id)).all()  # Fetch all users from the database
    result = []
    for user in users:
        image_url = url_for('static', filename=f'uploads/profiles/{user.user_profile_picture}', _external=True)
        result.append({
            'id': user.user_id,
            'f_name': user.user_first_name,
            'l_name': user.user_last_name,
            'phone': user.user_phone,
            'email': user.user_email,
            'status': 'Active' if user.user_is_active == 1 else 'Inactive',  # Set status based on user_is_active
            'photo': image_url
        })
        
    return jsonify(result), 201

# Add user
@app.route('/add-user', methods=['POST'])
def addUser():
    # Get form data
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    phone = request.form.get('phone')
    email = request.form.get('email')
    location = request.form.get('location')
    bio = request.form.get('bio')
    prefferred_genres = request.form.getlist('prefferred_genres[]')  # Get the array of preferred genres
    productImage = request.files.get('productImage')  # Get the uploaded image

    # Check if a user with the same phone number already exists
    similar_user = Users.query.filter_by(user_phone=phone, user_first_name = fname, user_last_name = lname).first()
    if similar_user:
        return jsonify({"message": "3"}), 200  # User already exists

    try:
        # Handle image upload
        if productImage:
            # Secure the filename and split extension
            original_filename = secure_filename(productImage.filename)
            name, ext = os.path.splitext(original_filename)

            # Convert extension to lowercase
            ext = ext.lower()

            # Validate the extension
            if ext.lstrip(".") not in ALLOWED_EXTENSIONS:
                return jsonify({"message": "4"}), 200  # Invalid extension

            # Create the final filename
            filename = f"{name}{ext}"

            # Open the image
            img = Image.open(productImage)

            # Convert RGBA to RGB if necessary
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Define target size (e.g., 200x200 for profile pictures)
            target_size = (200, 200)
            img_resized = img.resize(target_size, Image.Resampling.LANCZOS)

            # Ensure the upload folder exists
            os.makedirs(app.config['USERS_FOLDER'], exist_ok=True)

            # Save the resized image to the upload folder
            file_path = os.path.join(app.config['USERS_FOLDER'], filename)
            img_resized.save(file_path, "JPEG" if ext in {".jpg", ".jpeg"} else ext.lstrip("."))

            # Set the profile picture path in the database
            profile_picture_path = filename
        else:
            profile_picture_path = None  # No image uploaded

        # Create a new user object
        new_user = Users(
            user_first_name=fname,
            user_last_name=lname,
            user_phone=phone,
            user_email=email,
            user_location=location,
            user_bio=bio,
            user_preferred_genres=prefferred_genres,  # Add the preferred genres array
            user_profile_picture=profile_picture_path  # Add the profile picture path
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "1"}), 200  # User saved successfully

    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()  # Rollback in case of error
        return jsonify({"message": "2"}), 500  # Error saving the user

# delete book
@app.route('/del-user', methods=['POST'])
def delUser():
    data = request.get_json()
    book_id = data.get('id')

    # Query the `event_banner` column for the given `event_id`
    book_banner = db.session.query(BookProduct).with_entities(BookProduct.book_image).filter_by(book_id=book_id).first()

    # Access the result
    if book_banner:
        book_banner_value = book_banner[0]  # Get the `event_banner` value from the tuple
        folder_path = app.config['BOOKS_FOLDER']
        file_path = os.path.join(folder_path, book_banner_value)
        os.remove(file_path)

        # delete event details from db
        book = BookProduct.query.get(book_id)  
        if book:
            # If the category exists, delete it
            db.session.delete(book)
            db.session.commit() 
            return {"message": "1"}, 200
    else:
        return {"message": "2"}, 200 # error deleting