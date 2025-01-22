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
    return {"message": "1"}, 200

    try:
        # Secure the filename and split extension
        original_filename = secure_filename(productImage.filename)
        name, ext = os.path.splitext(original_filename)

        # Convert extension to lowercase
        ext = ext.lower()

        # Validate the extension
        if ext.lstrip(".") not in ALLOWED_EXTENSIONS:
            return {"message": f"Invalid file type: {ext}"}, 400

        # Create the final filename
        filename = f"{name}{ext}"

        # Open the image
        img = Image.open(productImage)

        # Convert RGBA to RGB if necessary
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Define target size (e.g., 1200x800 for blog banners)
        target_size = (600, 600)
        img_resized = img.resize(target_size, Image.Resampling.LANCZOS)

        # Ensure the upload folder exists
        os.makedirs(app.config['BOOKS_FOLDER'], exist_ok=True)

        # Save the resized image to the upload folder
        file_path = os.path.join(app.config['BOOKS_FOLDER'], filename)
        img_resized.save(file_path, "JPEG" if ext in {".jpg", ".jpeg"} else ext.lstrip("."))

        # Save blog details to the database
        new_blog = Blogs(
            blog_name=blog_name,
            blog_writer=blog_writer,
            blog_category=blog_category,
            blog_content=blog_content,
            productImage=filename
        )

        if new_blog:
            db.session.add(new_blog)
            db.session.commit()
            return {"message": "1"}, 200  # Blog saved successfully
        else:
            return {"message": "2"}, 404  # Error saving the blog

    except Exception as e:
        return {"message": f"Error processing image {productImage.filename}: {e}"}, 500