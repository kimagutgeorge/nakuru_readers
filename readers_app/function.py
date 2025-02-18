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
    category = BookCategory.query.filter_by(book_category_id=cat_id).first() 
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
    category = BookCategory.query.filter_by(book_category_id=cat_id).first() 
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
    collection = BookCollection.query.filter_by(book_collection_id=collection_id).first()  
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
    collection = BookCollection.query.filter_by(book_collection_id=cat_id).first() 
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
    password = request.form.get('password')
    role = request.form.get('role')
    bio = request.form.get('bio')
    prefferred_genres = request.form.getlist('genres[]')
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

        # store credentials for user
        login_user_id = new_user.user_id
        hashed_password = generate_password_hash(password)
        new_login = Login(
            login_user_id = login_user_id,
            login_password = hashed_password,
            login_user_role = role
        )
        db.session.add(new_login)
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

# view user
@app.route('/get-user', methods=['POST'])
def getUser():
    data = request.get_json()
    user_id = data.get("id")

    if not user_id:
        return jsonify({"message": "User ID is required"}), 400

    try:
        # Fetch the user details
        user = Users.query.filter_by(user_id=user_id).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        # Fetch preferred genres
        preferred_genres = []
        wishlist = []
        if user.user_wishlist:
            wishlist_ids = user.user_wishlist
            wishlist = (
                db.session.query(BookCategory.book_category_id, BookCategory.book_category_name)
                .filter(BookCategory.book_category_id.in_(wishlist_ids))
                .all()
            )
            wishlist = [{"name": single_list.book_category_name, "id": single_list.book_category_id} for single_list in wishlist]
        if user.user_preferred_genres:
            # Convert JSON array of genre IDs to a list of genre names
            genre_ids = user.user_preferred_genres
            preferred_genres = (
                db.session.query(BookCategory.book_category_id, BookCategory.book_category_name)
                .filter(BookCategory.book_category_id.in_(genre_ids))
                .all()
            )
            preferred_genres = [{"name": genre.book_category_name, "id": genre.book_category_id} for genre in preferred_genres]
        image_url = url_for('static', filename=f'uploads/profiles/{user.user_profile_picture}', _external=True)
        # Prepare the response
        if user.user_is_active == 1:
            user_status = 'Inactive'
        else:
            user_status = 'Active'

        if user.user_is_verified == 1:
            user_verified = 'Verified'
        else:
            user_verified = 'Unverified'
        
        if user.user_role == 1:
            user_role = 'Member'
        else:
            user_role = 'Admin'

        user_details = {
            'id': user.user_id,
            'f_name': user.user_first_name,
            'l_name': user.user_last_name,
            'phone': user.user_phone,
            'email': user.user_email,
            'location': user.user_location,
            'bio': user.user_bio,
            'photo': image_url,
            'reg': user.user_registration_date,
            'is_verified': user_verified,
            'is_active': user_status,
            'last_login': user.user_last_login,
            'last_active': user.user_last_active,
            'books': user.user_total_books_read,
            'role': user_role,
            'notifications': user.user_unread_notifications,
            'preferred_genres': preferred_genres,
            'wishlist': wishlist
        }

        return jsonify(user_details), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "An error occurred while fetching user details"}), 500
    
# edit user
@app.route('/edit-user', methods=['POST'])
def editUser():
    user_id = request.form.get("user_id")
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    phone = request.form.get('phone')
    email = request.form.get('email')
    location = request.form.get('location')
    bio = request.form.get('bio')
    prefferred_genres = request.form.getlist('genres[]')
    if not prefferred_genres:
        prefferred_genres = None
    
    # prefferred_genres_str = str(prefferred_genres).replace("[", "").replace("]", "")
    productImage = request.files.get('productImage')

    try:
        # Start a transaction
        with db.session.begin():
            # Fetch the book with row-level locking
            user = db.session.execute(
                select(Users)
                .where(Users.user_id == user_id)
                .with_for_update()
            ).scalar_one()

            if user:
                # Update the product details
                if productImage:
                    user_photo = db.session.query(Users).with_entities(Users.user_profile_picture).filter_by(user_id=user_id).first()

                    # Access the result
                    if user_photo:
                        user_photo_value = user_photo[0]  # Get the `event_banner` value from the tuple
                        folder_path = app.config['USERS_FOLDER']
                        file_path = os.path.join(folder_path, user_photo_value)
                        os.remove(file_path)
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

                    # update data
                    user.user_first_name=fname,
                    user.user_last_name=lname,
                    user.user_phone=phone,
                    user.user_email=email,
                    user.user_location=location,
                    user.user_bio=bio,
                    user.user_preferred_genres=prefferred_genres,  # Add the preferred genres array
                    user.user_profile_picture=profile_picture_path  # Add the profile picture path
                else:
                    # if no profile
                    # update data
                    user.user_first_name=fname,
                    user.user_last_name=lname,
                    user.user_phone=phone,
                    user.user_email=email,
                    user.user_location=location,
                    user.user_bio=bio,
                    user.user_preferred_genres=prefferred_genres,  # Add the preferred genres array

                # Commit the changes (implicitly done by the context manager)
                return {"message": "1"}, 200
            else:
                return {"message": "2"}, 200
    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        return {"message": f"An error occurred: {str(e)}"}, 500

# add event
@app.route('/add-event', methods=['POST'])
def addEvent():
    title = request.form.get("title")
    description = request.form.get('description')
    date_time = request.form.get('date_time')
    location = request.form.get('location')
    event_link = request.form.get('event_link')
    
    # Check if the category already exists
    existing_event = Events.query.filter_by(event_title=title).first()
    if existing_event:
        return {"message": "3"}, 201  # Event exists

    # Create a new Category instance
    new_event = Events(event_title=title, event_description=description, event_date_time = date_time, event_location = location, event_link = event_link)
    
    # Add the new category to the session
    db.session.add(new_event)
    
    # Commit the session to save it in the database
    db.session.commit()

    return {"message": "1"}, 201  # Created status code
    
# get events
@app.route('/get-events', methods=['GET'])
def getEvents():
    # Fetch all users and format the result
    events = Events.query.order_by(desc(Events.event_id)).all()  # Fetch all events from the database
    result = []
    for event in events:
        result.append({
            'id': event.event_id,
            'title': event.event_title,
            'description': event.event_description,
            'time': event.event_date_time,
            'location': event.event_location,
            'link': event.event_link,
            'status': 'COMPLETE' if event.event_status == 1 else 'PENDING' if event.event_status == 0 else 'CANCELLED' # Set status based on user_is_active
        })
        
    return jsonify(result), 201

# view event
@app.route('/get-event', methods = ['POST'])
def viewEvent():
    data = request.get_json()
    id = data.get("event_id")
    
    # events = db.session.query(Events).join(BookCategory, BookProduct.book_genre == BookCategory.book_category_id).join(BookCollection, BookProduct.book_collection == BookCollection.book_collection_id).filter(BookProduct.book_id == id)
    events = Events.query.order_by(desc(Events.event_id)).filter(Events.event_id == id)
    # Build the result with image URLs
    attendees = []
    result = []
    for event in events:
        if event.event_attendees:
            # Convert JSON array of genre IDs to a list of genre names
            users_ids = event.event_attendees
            attendees = (
                db.session.query(Users.user_id, Users.user_first_name, Users.user_last_name)
                .filter(Users.user_id.in_(users_ids))
                .all()
            )
            attendees = [{"fname": attendee.user_first_name, "lname": attendee.user_last_name} for attendee in attendees]
        # end of attendees
        result.append({
            'title': event.event_title,
            'description': event.event_description,
            'time': event.event_date_time,
            'location': event.event_location,
            'link': event.event_link,
            'attendees': attendees,
            'status': 'COMPLETE' if event.event_status == 1 else 'PENDING' if event.event_status == 0 else 'CANCELLED' # Set status based on user_is_active
        })
    
    return jsonify(result), 201

# update event
@app.route('/edit-event', methods=['POST'])
def editEvent():
    event_id = request.form.get("id")
    title = request.form.get("title")
    description = request.form.get('description')
    date_time = request.form.get('date_time')
    location = request.form.get('location')
    event_link = request.form.get('event_link')
    status = request.form.get('status')
    attendees = request.form.getlist('attendees[]')
    if not status:
        status = '0'

    try:
        # Start a transaction
        with db.session.begin():
            # Fetch the book with row-level locking
            event = db.session.execute(
                select(Events)
                .where(Events.event_id == event_id)
                .with_for_update()
            ).scalar_one()

            if event:
                if attendees:
                    # Update the product details
                    event.event_title = title
                    event.event_description = description
                    event.event_date_time = date_time
                    event.event_location = location
                    event.event_link = event_link
                    event.event_status = status
                    event.event_attendees = attendees
                # if attendees is empty
                else:
                    # Update the product details
                    event.event_title = title
                    event.event_description = description
                    event.event_date_time = date_time
                    event.event_location = location
                    event.event_link = event_link
                    event.event_status = status
                # Commit the changes (implicitly done by the context manager)
                return {"message": "1"}, 200
            else:
                return {"message": "2"}, 200
    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        return {"message": f"An error occurred: {str(e)}"}, 500

# delete event
@app.route('/del-event', methods = ['POST'])
def deleteEvent():
    data = request.get_json()
    event_id = data.get('id')

    # Fetch the event by its ID
    event = Events.query.filter_by(event_id=event_id).first()  
    if event:
        # If the event exists, delete it
        db.session.delete(event)
        db.session.commit() 
        return {"message": "1"}, 200
    else:
        return {"message": "2"}, 200

# add rule
@app.route('/add-rule', methods = ['POST'])
def addRule():
    rule_id = request.form.get('id')
    title = request.form.get("title")
    description = request.form.get("description")
    # check if it's an update
    if rule_id:
         # Fetch the category by its ID
        existing_rule = Rules.query.filter_by(rule_id = rule_id).first()
        if existing_rule:
            # Update the name
            existing_rule.rule_title = title
            existing_rule.rule_description = description
            # Commit the changes
            db.session.commit() 
            return {"message": "1"}, 200 # updated
        else:
            return {"message": "2"}, 200 # failed
    else:
        # check if rule exists
        existing_rule = Rules.query.filter_by(rule_title = title).first()
        if existing_rule:
            return {"message": "3"}, 200
        else:
            new_rule = Rules(
                rule_title = title,
                rule_description = description
            )
            db.session.add(new_rule)
            db.session.commit()
            return {"message": "1"}, 200 # saved

# get rules
@app.route('/get-rules', methods = ['GET'])
def getRules():
    rules = Rules.query.order_by(desc(Rules.rule_id)).all()  # Fetch all rules from the database
    result = [{'id': rule.rule_id, 'title': rule.rule_title, 'description': rule.rule_description } for rule in rules]
    return jsonify(result), 201

# delete rules
@app.route('/del-rule', methods = ['POST'])
def deleteRule():
    data = request.get_json()
    rule_id = data.get('rule_id')

    # Fetch the rule by its ID
    rule = Rules.query.filter_by(rule_id=rule_id).first() 
    if rule:
        # If the rule exists, delete it
        db.session.delete(rule)
        db.session.commit() 
        return {"message": "1"}, 200
    else:
        return {"message": "2"}, 200

# add read
@app.route('/add-read', methods = ['POST'])
def addRead():
    description = request.form.get('description')
    genre = request.form.get('genre')
    bookName = request.form.get('bookName')
    productImage = request.files['productImage']
    bookFile = request.files['bookFile']  # PDF file
    collection = request.form.get('collection')

    if not collection:
        collection = '1'

    similar_book = db.session.query(Reads).filter(Reads.read_name == bookName).first()

    if similar_book:
        return {"message": "3"}, 200  # Book already exists
    
    else:
        try:
            # Secure the filename and split extension for the image
            original_image_filename = secure_filename(productImage.filename)
            image_name, image_ext = os.path.splitext(original_image_filename)
            
            # Convert image extension to lowercase
            image_ext = image_ext.lower()

            # Validate the image extension
            if image_ext.lstrip(".") not in ALLOWED_EXTENSIONS:
                return {"message": "4"}, 200  # invalid extension

            # Create the final image filename
            image_filename = f"{image_name}{image_ext}"

            # Open the image
            img = Image.open(productImage)

            # Convert RGBA to RGB if necessary
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Define target size (e.g., 800x800)
            target_size = (800, 800)
            img_resized = img.resize(target_size, Image.Resampling.LANCZOS)

            # Ensure the upload folder exists
            os.makedirs(app.config['COVERS_FOLDER'], exist_ok=True)
            os.makedirs(app.config['READS_FOLDER'], exist_ok=True)

            # Save the resized image to the upload folder
            image_file_path = os.path.join(app.config['COVERS_FOLDER'], image_filename)
            img_resized.save(image_file_path, "JPEG" if image_ext in {".jpg", ".jpeg"} else image_ext.lstrip("."))

            # Handle the PDF file
            original_pdf_filename = secure_filename(bookFile.filename)
            pdf_name, pdf_ext = os.path.splitext(original_pdf_filename)

            # Validate the PDF extension
            if pdf_ext.lower() != ".pdf":
                return {"message": "5"}, 200  # invalid PDF extension

            # Create the final PDF filename
            pdf_filename = f"{pdf_name}{pdf_ext}"

            # Save the PDF file to the upload folder
            pdf_file_path = os.path.join(app.config['READS_FOLDER'], pdf_filename)
            bookFile.save(pdf_file_path)

            # Save book details to the database
            new_book = Reads(
                read_genre=genre,
                read_name=bookName,
                read_image=image_filename,
                read_collection=collection,
                read_description=description,
                read_file=pdf_filename  # Save the PDF filename to the database
            )

            if new_book:
                db.session.add(new_book)
                db.session.commit()
                return {"message": "1"}, 200  # book saved successfully
            else:
                return {"message": "2"}, 100  # Error saving the book

        except Exception as e:
            print(e)
            return {"message": "3"}, 200  # error processing image or PDF

# get reads
@app.route('/get-reads', methods = ['GET'])
def getReads():
    reads = Reads.query.order_by(desc(Reads.read_id)).all()  # Fetch all products from the database
    # Build the result with image URLs
    result = []
    for book in reads:
        image_url = url_for('static', filename=f'uploads/book_covers/{book.read_image}', _external=True)
        result.append({
            'id': book.read_id,
            'name': book.read_name,
            'image': image_url
        })
    
    return jsonify(result), 201

# user login
@app.route('/login', methods=['POST'])
def login():
    # Collect info from frontend
    data = request.get_json()
    username = data.get('email')
    password = data.get('password')
    # Retrieve the user by username
    user = Login.query.filter_by(username=username).first()

    # Check if the user exists and the password is correct
    if user and check_password_hash(user.password_hash, password):
        session['user'] = user.username  # Set the username in session
        return {"message": "1"}, 200  # Return proper response
    else:
        return {"message": "2"}, 200  # Return unauthorized response

# add role
@app.route('/add-role', methods=['POST'])
def addRole():
    data = request.get_json()
    role_name = data.get('name')

    if role_name:
        # Check if the role already exists
        existing_name = Roles.query.filter_by(role_name=role_name).first()
        if existing_name:
            return {"message": "3"}, 201  # Conflict status code

        # Create a new role instance
        new_role = Roles(role_name=role_name)
        
        # Add the new role to the session
        db.session.add(new_role)
        
        # Commit the session to save it in the database
        db.session.commit()

        return {"message": "1"}, 201  # Created status code
    else:
        return {"message": "2"}, 201  # Bad request

# fetch roles
@app.route('/get-roles', methods=['GET'])
def getRoles():
    roles = Roles.query.order_by(desc(Roles.role_id)).all()  # Fetch all roles from the database
    result = [{'id': role.role_id, 'name': role.role_name } for role in roles]
    return jsonify(result), 201

# delete role
@app.route('/del-role', methods = ['POST'])
def delRole():
    data = request.get_json()
    role_id = data.get('id')

    # Fetch the role by its ID
    role = Roles.query.filter_by(role_id=role_id).first() 
    if role:
        # If the role exists, delete it
        db.session.delete(role)
        db.session.commit() 
        return {"message": "1"}, 200
    else:
        return {"message": "2"}, 200

# edit role
@app.route('/save-role', methods=['POST'])
def editRole():
    data = request.get_json()
    role_id = data.get('id')
    role_name = data.get('name')

    # Fetch the role by its ID
    role = Roles.query.filter_by(role_id=role_id).first() 
    if role:
         # Update the name
        role.role_name = role_name 
         # Commit the changes
        db.session.commit() 
        return {"message": "1"}, 200
    else:
        return {"message": "2"}, 200