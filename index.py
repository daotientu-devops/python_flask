from flask import Flask, request, make_response, abort
from flask.globals import session
from flask.helpers import flash, url_for
from flask.templating import render_template
from werkzeug.utils import redirect, secure_filename
import sqlite3 as sql
from forms import ContactForm
app = Flask(__name__)
app.secret_key = 'dadadadada';
@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All field are required')
            return render_template('contact.html', form = form)
        else:
            return render_template('success.html')
    if request.method == 'GET':
        return render_template('contact.html', form = form)        
@app.route('/')
def index():
    try:
        conn = sql.connect('database.db')
        print('Opened database successfully')
        conn.execute('CREATE TABLE students(name TEXT, addr TEXT, city TEXT, pin TEXT)')
        print('Table created successfully')
        conn.close()
    except:    
        return null
    finally:
        return render_template('home.html')
@app.route('/enternew')    
def new_student():
    return render_template('student.html')
@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students(name, addr, city, pin) VALUES (?,?,?,?)", (nm, addr, city, pin))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "Error in insert operation"  
        finally:
            con.close()       
            return render_template("result.html", msg = msg)
@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall();
    return render_template("list.html", rows = rows)
@app.route('/login', methods = ['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
            request.form['password'] != 'admin':
            error = 'Invalid username or password. Please try again!'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error = error)
@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))
@app.route('/upload')
def upload_file():
    return render_template('upload.html')
@app.route('/uploader', methods=['GET', 'POST'])
def uploader_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'File uploaded successfully'
if __name__ == '__main__':
    app.run(debug = False)