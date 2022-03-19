from flask import Flask,render_template, request, redirect,url_for
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
 
mysql = MySQL(app)
 
@app.route('/add')
def form():
    return render_template('add.html')
 
#  Add new customer
@app.route('/add', methods = ['POST'])
def add():
    name = request.form['name']
    age = request.form['age']
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(''' INSERT INTO customer(name,age) VALUES(%s,%s)''',(name,age))
    conn.commit()
    cursor.close()
    # return f"Added Successfully"
    return redirect(url_for('get'))

#  Home : shows a table of all customers 
@app.route('/')
def get():
    try:
        conn = mysql.connection
        cursor = conn.cursor() 
        cursor.execute("SELECT * FROM customer")
        rows = cursor.fetchall()
        return render_template('customers.html', value=rows)
    except Exception as e:
        print(e)
        return f"An error has occured"
    finally:
        cursor.close() 

#  form to edit the customer 
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_customer(id):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customer WHERE user_id = %s', (id))
    row = cursor.fetchone()
    cursor.close()
    return render_template('edit.html', row = row)

#   updating the customer on DB
@app.route('/update/<id>', methods=['POST'])
def update_customer(id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("""UPDATE customer
            SET name = %s, age = %s WHERE user_id = %s """, (name, age, id))
        conn.commit()
        # return f'UPDATE SUCCESS'
        return redirect(url_for('get'))

#   Delete customer
@app.route('/delete/<id>', methods = ['POST','GET'])
def delete_customer(id):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(""" DELETE FROM customer WHERE user_id = %s """, (id))
    conn.commit()
    # return f'DELETE SUCCESS'
    return redirect(url_for('get'))



 
app.run(host='localhost', port=5000)
