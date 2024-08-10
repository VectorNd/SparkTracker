from flask import Flask, jsonify, request, redirect, url_for, flash, session
from flask import render_template 
from OtherFunctions.SQL_Functions import Database

app = Flask(__name__)
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

db = Database()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        number = request.form['number']
        check_freq = request.form['check_freq']

        print(username , email , number , check_freq)

        # Check if user exists in the database
        with Database() as db:
            user_data = db.access_user_data()
            print(user_data)
            if user_data and user_data[0] == username and user_data[1] == email and user_data[2] == number and user_data[3] == check_freq:
                session['user'] = username
                flash('Logged in successfully.', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid login credentials.', 'danger')
                return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        number = request.form['number']
        check_freq = request.form['check_freq']
        
        with Database() as db:
           db.get_user_data(username, email, number, check_freq)
        flash('You have successfully registered. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/', methods=['GET'])
def index():
    if 'user' in session:
        with Database() as db:
            user_data = db.access_user_data()
            product_params = db.access_product_params()
        return render_template('index.html', user_data=user_data, product_params=product_params)
    else:
        return redirect(url_for('login'))

@app.route('/add_product', methods=['POST'])
def add_product():
    url = request.form['url']
    max_price = request.form['max_price']

    with Database() as db:
       db.get_product_params(url, max_price)
    return redirect(url_for('index'))

@app.route('/remove_product/<int:product_id>', methods=['POST'])
def remove_product(product_id):
    with Database() as db:
       db.remove_product(product_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)