from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
import sys
  
  
app = Flask(__name__)
   
app.secret_key = 'abcd2123445'  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'library-system'
  
mysql = MySQL(app)
  
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['id']
            session['name'] = user['first_name']
            session['email'] = user['email']
            session['role'] = user['role']
            mesage = 'Logged in successfully !'            
            return redirect(url_for('books'))
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)
    
@app.route("/users", methods =['GET', 'POST'])
def users():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user')
        users = cursor.fetchall()    
        return render_template("users.html", users = users)
    return redirect(url_for('login'))

@app.route("/save_user", methods =['GET', 'POST'])
def save_user():
    msg = ''    
    if 'loggedin' in session:        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST' and 'role' in request.form and 'first_name' in request.form and 'last_name' in request.form and 'email' in request.form :
            
            first_name = request.form['first_name']  
            last_name = request.form['last_name'] 
            email = request.form['email']            
            role = request.form['role']             
            action = request.form['action']
            
            if action == 'updateUser':
                userId = request.form['userid']                 
                cursor.execute('UPDATE user SET first_name= %s, last_name= %s, email= %s, role= %s WHERE id = %s', (first_name, last_name, email, role, (userId, ), ))
                mysql.connection.commit()   
            else:
                password = request.form['password'] 
                cursor.execute('INSERT INTO user (`first_name`, `last_name`, `email`, `password`, `role`) VALUES (%s, %s, %s, %s, %s)', (first_name, last_name, email, password, role))
                mysql.connection.commit()   

            return redirect(url_for('users'))        
        elif request.method == 'POST':
            msg = 'Please fill out the form !'        
        return redirect(url_for('users'))      
    return redirect(url_for('login'))

@app.route("/edit_user", methods =['GET', 'POST'])
def edit_user():
    msg = ''    
    if 'loggedin' in session:
        editUserId = request.args.get('userid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE id = % s', (editUserId, ))
        users = cursor.fetchall()         

        return render_template("edit_user.html", users = users)
    return redirect(url_for('login'))

    
@app.route("/view_user", methods =['GET', 'POST'])
def view_user():
    if 'loggedin' in session:
        viewUserId = request.args.get('userid')   
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE id = % s', (viewUserId, ))
        user = cursor.fetchone()   
        return render_template("view_user.html", user = user)
    return redirect(url_for('login'))
    
@app.route("/password_change", methods =['GET', 'POST'])
def password_change():
    mesage = ''
    if 'loggedin' in session:
        changePassUserId = request.args.get('userid')        
        if request.method == 'POST' and 'password' in request.form and 'confirm_pass' in request.form and 'userid' in request.form  :
            password = request.form['password']   
            confirm_pass = request.form['confirm_pass'] 
            userId = request.form['userid']
            if not password or not confirm_pass:
                mesage = 'Please fill out the form !'
            elif password != confirm_pass:
                mesage = 'Confirm password is not equal!'
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE user SET  password =% s WHERE id =% s', (password, (userId, ), ))
                mysql.connection.commit()
                mesage = 'Password updated !'            
        elif request.method == 'POST':
            mesage = 'Please fill out the form !'        
        return render_template("password_change.html", mesage = mesage, changePassUserId = changePassUserId)
    return redirect(url_for('login'))   
    
@app.route("/delete_user", methods =['GET'])
def delete_user():
    if 'loggedin' in session:
        deleteUserId = request.args.get('userid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM user WHERE userid = % s', (deleteUserId, ))
        mysql.connection.commit()   
        return redirect(url_for('users'))
    return redirect(url_for('login'))
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL,NULL,% s, % s, % s,NULL)', (userName, email, password, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)

# Manage Books   
@app.route("/books", methods =['GET', 'POST'])
def books():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT book.bookid, book.picture, book.name, book.status, book.isbn, book.no_of_copy, book.updated_on FROM book")
        books = cursor.fetchall()    
        return render_template("books.html", books = books)
    return redirect(url_for('login'))
    
@app.route("/edit_book", methods =['GET', 'POST'])
def edit_book():
    msg = ''    
    if 'loggedin' in session:
        editBookId = request.args.get('bookid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT book.bookid, book.picture, book.name, book.status, book.isbn, book.no_of_copy, book.updated_on FROM book WHERE book.bookid = % s', (editBookId, ))
        books = cursor.fetchall()     
        return render_template("edit_books.html", books = books)
    return redirect(url_for('login'))

@app.route("/save_book", methods =['GET', 'POST'])
def save_book():
    msg = ''    
    if 'loggedin' in session:
        editUserId = request.args.get('userid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT book.bookid, book.picture, book.name, book.status, book.isbn, book.no_of_copy, book.updated_on FROM book")
        books = cursor.fetchall() 
        if request.method == 'POST' and 'name' in request.form :
            bookName = request.form['name'] 
            isbn = request.form['isbn']  
            no_of_copy = request.form['no_of_copy']            
            status = request.form['status']
            action = request.form['action']
            
            if action == 'updateBook':
                bookId = request.form['bookid']
                cursor.execute('UPDATE book SET name= %s, status= %s, isbn= %s, no_of_copy= %s WHERE bookid = %s', (bookName, status, isbn, no_of_copy, (bookId, ), ))
                mysql.connection.commit()   
            else:
                cursor.execute('INSERT INTO book (`name`, `status`, `isbn`, `no_of_copy`) VALUES (%s, %s, %s, %s, %s, %s)', (bookName, status, isbn, no_of_copy))
                mysql.connection.commit()           
            return redirect(url_for('books'))        
        elif request.method == 'POST':
            msg = 'Please fill out the form !'        
        return render_template("books.html", msg = msg, books = books)
    return redirect(url_for('login'))
    
@app.route("/delete_book", methods =['GET'])
def delete_book():
    if 'loggedin' in session:
        deleteBookId = request.args.get('bookid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM book WHERE bookid = % s', (deleteBookId, ))
        mysql.connection.commit()   
        return redirect(url_for('books'))
    return redirect(url_for('login'))    
    
# Manage issue book   
@app.route("/list_issue_book", methods =['GET', 'POST'])
def list_issue_book():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT issued_book.issuebookid, issued_book.issue_date_time, issued_book.expected_return_date,  issued_book.return_date_time, issued_book.status, book.name As book_name, book.isbn, user.first_name, user.last_name FROM issued_book LEFT JOIN book ON book.bookid = issued_book.bookid LEFT JOIN user ON user.id = issued_book.userid")
        issue_books = cursor.fetchall() 

        cursor.execute("SELECT bookid, name FROM book")
        books = cursor.fetchall()

        cursor.execute("SELECT id, first_name, last_name FROM user")
        users = cursor.fetchall()        

        return render_template("issue_book.html", issue_books = issue_books, books = books, users = users)
    return redirect(url_for('login')) 

@app.route("/save_issue_book", methods =['GET', 'POST'])
def save_issue_book():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT issued_book.issuebookid, issued_book.issue_date_time, issued_book.expected_return_date,  issued_book.return_date_time, issued_book.status, book.name As book_name, book.isbn, user.first_name, user.last_name FROM issued_book LEFT JOIN book ON book.bookid = issued_book.bookid LEFT JOIN user ON user.id = issued_book.userid")
        issue_books = cursor.fetchall() 

        if request.method == 'POST' and 'book' in request.form and 'users' in request.form and 'expected_return_date' in request.form and 'return_date' in request.form and 'status' in request.form:
            bookId = request.form['book'] 
            userId = request.form['users']  
            expected_return_date = request.form['expected_return_date'] 
            return_date = request.form['return_date']
            status = request.form['status'] 
            action = request.form['action']             
            
            if action == 'updateIssueBook':
                issuebookid = request.form['issueBookId'] 
                cursor.execute('UPDATE issued_book SET bookid = %s, userid = %s, expected_return_date = %s, return_date_time = %s, status = %s WHERE issuebookid =% s', (bookId, userId, expected_return_date, return_date, status, (issuebookid, ), ))
                mysql.connection.commit()        
            else: 
                cursor.execute('INSERT INTO issued_book (`bookid`, `userid`, `expected_return_date`, `return_date_time`, `status`) VALUES (%s, %s, %s, %s, %s)', (bookId, userId, expected_return_date, return_date, status))
                mysql.connection.commit()        
            return redirect(url_for('list_issue_book'))        
        elif request.method == 'POST':
            msg = 'Please fill out the form !'        
        return redirect(url_for('list_issue_book'))
    return redirect(url_for('login')) 

@app.route("/edit_issue_book", methods =['GET', 'POST'])
def edit_issue_book():
    msg = ''    
    if 'loggedin' in session:
        issuebookid = request.args.get('issuebookid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT issued_book.issuebookid, issued_book.issue_date_time, issued_book.expected_return_date,  issued_book.return_date_time, issued_book.bookid, issued_book.userid, issued_book.status, book.name As book_name, book.isbn, user.first_name, user.last_name FROM issued_book LEFT JOIN book ON book.bookid = issued_book.bookid LEFT JOIN user ON user.id = issued_book.userid WHERE issued_book.issuebookid = %s', (issuebookid,))
        issue_books = cursor.fetchall()  

        cursor.execute("SELECT bookid, name FROM book")
        books = cursor.fetchall()

        cursor.execute("SELECT id, first_name, last_name FROM user")
        users = cursor.fetchall()   

        return render_template("edit_issue_book.html", issue_books = issue_books, books = books, users = users)
    return redirect(url_for('login'))

@app.route("/delete_issue_book", methods =['GET'])
def delete_issue_book():
    if 'loggedin' in session:
        issuebookid = request.args.get('issuebookid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM issued_book WHERE issuebookid = % s', (issuebookid, ))
        mysql.connection.commit()   
        return redirect(url_for('list_issue_book'))
    return redirect(url_for('login'))
 

    
if __name__ == "__main__":
    app.run()
    os.execv(__file__, sys.argv)

