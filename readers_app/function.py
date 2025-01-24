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
    result = [{'id': category.book_category_id, 'name': category.book_category_name} for category in categories]
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

# get product session
@app.route('/product-to-view', methods = ['POST'])
def getProductSession():
    data = request.get_json()
    session["product_id"] = data.get('product_id')
    return {"message": "1"}, 200 # session created