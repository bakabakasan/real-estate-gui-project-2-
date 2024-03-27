from flask import Flask, render_template, jsonify, request, redirect
import sqlite3

app = Flask(__name__)

# Функция для создания соединения с базой данных
def create_db_connection():
    try:
        connection = sqlite3.connect('database.db')
        print("Connected to the database.")
        return connection
    except sqlite3.Error as e:
        print("An error occurred while connecting to the database:", str(e))
        return None

# Функция для загрузки данных из таблицы "estate"
def load_estate_from_db(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM estate")
        rows = cursor.fetchall()
        print("Fetched rows from the database:", rows)
        cursor.close()
        return rows
    except sqlite3.Error as e:
        print("An error occurred while executing the query:", str(e))
        return None

# Функция для загрузки данных из таблицы "estate" по ID
def load_estateitem_from_db(connection, id):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM estate WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            keys = [description[0] for description in cursor.description]
            row_dict = dict(zip(keys, row))
            cursor.close()
            return row_dict
        else:
            cursor.close()
            return None
    except sqlite3.Error as e:
        print("An error occurred while executing the query:", str(e))
        return None

# Функция для добавления сообщения в таблицу "messages"
def add_message_to_db(connection, page_url, data):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO messages(full_name, phone_number, email, message, page_url) 
            VALUES(?, ?, ?, ?, ?)""",
            (data.get('full_name', ''),  
             data.get('phone_number', ''),  
             data.get('email', ''),  
             data.get('message', ''),  
             page_url)
        )
        connection.commit()
        print("Message added to the database successfully.")
        cursor.close()
    except sqlite3.Error as e:
        print("An error occurred while adding the message to the database:", str(e))
        raise  # Re-raise the exception for handling in Flask view

# Функция для загрузки данных из таблицы "messages"
def load_messages_from_db(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM messages")
        rows = cursor.fetchall()
        print("Fetched rows from the database:", rows)
        cursor.close()
        return rows
    except sqlite3.Error as e:
        print("An error occurred while executing the query:", str(e))
        return None

# Функция для регистрации нового пользователя
def register_user(connection, name, email, password):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO users(name, email, password)
            VALUES(?, ?, ?)""", (name, email, password))
        connection.commit()
        print("User was added to the database successfully.")
        cursor.close()
    except sqlite3.Error as e:
        print("An error occurred while adding the user to the database:", str(e))

# Функция для аутентификации пользователя
def authenticate_user(connection, email, password):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM users
            WHERE email = ? AND password = ?""", (email, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print("An error occurred while authenticating user:", str(e))
        return False

# Использование функций
connection = create_db_connection()
if connection:
    estate = load_estate_from_db(connection)
    estate_item = load_estateitem_from_db(connection, id)
    add_message_to_db(connection, page_url, data)
    messages = load_messages_from_db(connection)
    register_user(connection, name, email, password)
    authenticate_user(connection, email, password)
else:
    print("Failed to connect to the database.")


@app.route("/") 
def hello_dreamhouse(): 
    try:
        estate = load_estate_from_db(connection)
        return render_template('home.html', estate=estate) 
    except Exception as e:
        return render_template('error.html', error=str(e)), 500

@app.route("/api/estate")
def list_estate():
    try:
        estates = load_estate_from_db(connection)
        return jsonify(estate=estates)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route("/estateitem/<id>")
def show_estate(id):
    try:
        estate_item = load_estateitem_from_db(connection, id)
        if not estate_item:
            return "Not Found", 404
        return render_template('estatepage.html', estate=estate_item)
    except Exception as e:
        return render_template('error.html', error=str(e)), 500

@app.route("/sent-message", methods=['POST'])
def fill_in_the_form():
    try:
        data = request.form
        page_url = request.referrer  # Get the referrer URL
        if page_url is None:
            raise ValueError("Referrer URL is not provided.")

        print("Referrer URL:", page_url)
        print("Form Data:", data)
        add_message_to_db(connection, page_url, data)  # Pass page_url to the function
        return render_template('sent_message.html', data=data)
    except Exception as e:
        return render_template('error.html', error=str(e)), 500



@app.route("/requests") 
def all_sent_requests():
    try:
        messages = load_messages_from_db(connection)
        return render_template('requests.html', messages=messages) 
    except Exception as e:
        return render_template('error.html', error=str(e)), 500

@app.route("/contacts") 
def contact_details(): 
    return render_template('contacts.html')

@app.route("/about-us") 
def about_company(): 
    return render_template('aboutus.html')

@app.route("/register", methods=['GET', 'POST']) 
def register(): 
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')

            if not name or not email or not password:
                return render_template('error.html', error='Please fill out all fields'), 400

            register_user(connection, name, email, password)

            return redirect('/login')

        return render_template('register.html') 
    except Exception as e:
        return render_template('error.html', error=str(e)), 500

@app.route("/login", methods=['GET', 'POST']) 
def login():
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            if authenticate_user(connection, email, password):
                return redirect('/')
            else:
                return render_template('login.html', error='Invalid email or password')

        return render_template('login.html')
    except Exception as e:
        return render_template('error.html', error=str(e)), 500  

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)