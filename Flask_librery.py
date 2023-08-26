# This web application was developed using the Flask framework and Python.
# The purpose of the application is to manage data related to books and customers in the library.
# The application has several key products such as adding new customers and customers,
# displaying lists of books and customers, displaying special records, and deleting books.

# Flask
from flask import Flask, render_template, request, render_template_string
from psycopg2 import connect, OperationalError

app = Flask(__name__)  # Initialize a Flask web application instance.
database_name = 'library_db'

# HTML form for deleting a book.
formularz_kasowania = """ 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
<h1>{books}</h1>
<form action="#" method="post">
    <label>
        <input type="submit" value="Delete">
    </label>
</form>
</body>
</html> 
"""

# Route to add a new book via a form.
@app.route('/book/add', methods=['GET', 'POST'])
def add_book():
# Function to handle adding a book to the database
    if request.method == 'GET':
        return render_template('book_add.html')

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        isbn = request.form.get('ISBN')

        try:
            cnx = connect(user="postgres", password="coderslab", host="localhost", database="library_db")
            cnx.autocommit = True
            cursor = cnx.cursor()
            sql = "INSERT INTO Book(name, description, isbn) VALUES (%s, %s, %s)"
            values = (name, description, isbn)
            cursor.execute(sql, values)
            cnx.close()
            cursor.close()
            return "Book added!"
        except OperationalError as e:
            return "Invalid data!", e

# Route to list all books in the database.
@app.route('/book', methods=["GET"])
# Function to retrieve and display a list of books
def books_list():
    try:
        cnx = connect(user="postgres", password="coderslab", host="localhost", database="library_db")
        cnx.autocommit = True
        cursor = cnx.cursor()
        sql = "SELECT * FROM Book;"
        cursor.execute(sql)
        # books = cursor.fetchall()
        books = [row for row in cursor]
        cnx.close()
        cursor.close()
        return render_template('List_of_books.html', books=books)
    except OperationalError as e:
        return "Invalid data!", e

# Route to display details of a specific book.
@app.route('/book/<book_id>', methods=["GET"])
def books(book_id):
# Function to retrieve and display details of a specific book
    try:
        cnx = connect(user="postgres", password="coderslab", host="localhost", database="library_db")
        cnx.autocommit = True
        cursor = cnx.cursor()
        sql = f"SELECT * FROM Book WHERE id={book_id}";
        cursor.execute(sql)
        books = [row for row in cursor]
        # books = cursor.fetchall()
        cnx.close()
        cursor.close()
        if books != []:
            books = books[0]
            return render_template("details_book.html", books=books)
        return f'There is no id book = {book_id}'
    except OperationalError as e:
        return "Invalid data!", e

# Route to show a confirmation page for deleting a book.
@app.route('/book/del/<book_id>', methods=['GET', 'POST'])
def delete_movie(book_id):
# Function to show a confirmation page and delete a book.
    if request.method == 'GET':
        try:
            cnx = connect(user="postgres", password="coderslab", host="localhost", database="library_db")
            cnx.autocommit = True
            cursor = cnx.cursor()
            sql = f"SELECT * FROM Book WHERE id={book_id};"
            cursor.execute(sql)
            # books = cursor.fetchall()
            books = [row for row in cursor]
            cnx.close()
            cursor.close()
            if books != []:
                books = books[0]
                return formularz_kasowania.format(books=books)
            return f'There is no id book = {book_id}'
        except OperationalError as e:
            return "Invalid data!", e
    elif request.method == 'POST':
        cnx = connect(user="postgres", password="coderslab", host="localhost", database="library_db")
        cnx.autocommit = True
        cursor = cnx.cursor()
        sql = f"DELETE FROM Book WHERE id={book_id};"
        cursor.execute(sql)
        cnx.close()
        cursor.close()
        return 'the book has been removed'


# Route to add a new client (reader) via a form.
@app.route('/book/client/add', methods=['GET', 'POST'])
def add_client():
    # (Function to handle adding a client to the database
    if request.method == 'GET':
        return render_template('client_add.html')

    if request.method == 'POST':
        name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        try:
            cnx = connect(user="postgres", password="coderslab", host="localhost", database="library_db")
            cnx.autocommit = True
            cursor = cnx.cursor()
            sql = "INSERT INTO client(first_name, last_name) VALUES (%s, %s)"
            values = (name, last_name)
            cursor.execute(sql, values)
            cnx.close()
            cursor.close()
            return "Client added!"
        except OperationalError as e:
            return "Invalid data!", e

# Route to list all clients in the database
@app.route('/book/client', methods=["GET"])
def client_list():
# Function to retrieve and display a list of clients
    try:
        cnx = connect(user="postgres", password="coderslab", host="localhost", database="library_db")
        cnx.autocommit = True
        cursor = cnx.cursor()
        sql = "SELECT * FROM client;"
        cursor.execute(sql)
        # client = cursor.fetchall()
        client = [row for row in cursor]
        cnx.close()
        cursor.close()
        return render_template("client_index.html", client=client)
    except OperationalError as e:
        return "Invalid data!", e


# Route to display details of a specific client
@app.route('/book/client/<client_id>', methods=["GET"])
# Function to retrieve and display details of a specific client
def client_id(client_id):
    try:
        cnx = connect(user="postgres", password="coderslab", host="localhost", database="library_db")
        cnx.autocommit = True
        cursor = cnx.cursor()
        sql = f"SELECT * FROM client WHERE id={client_id};"
        cursor.execute(sql)
        client = [row for row in cursor]
        # books = cursor.fetchall()
        cnx.close()
        cursor.close()
        if client != []:
            client = client[0]
            return render_template('client_detail.html', client=client)
        return f'Nie ma ksiażki o id = {client_id}'
    except OperationalError as e:
        return "Invalid data!", e


# Run the Flask application.
if __name__ == '__main__':
    app.run(debug=True)






