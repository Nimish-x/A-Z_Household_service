from flask import Flask, request, flash, session, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_not_key'
DATABASE = 'SQLlite/app_database.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    return db

@app.route('/')
def home():
    return redirect(url_for('login_details'))

@app.route('/login', methods=['POST', 'GET'])
def login_details():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM customer WHERE username=? AND password=?""", (username, password))
        user1 = cursor.fetchone()
        cursor.execute("""select service_name, Prof_name, Prof_phone, status, id from service_history where username=?""",(username,))
        service_user1=cursor.fetchall()
        prices = []
        for history in service_user1:
            service_name = history[0]
            cursor.execute("""
                SELECT price 
                FROM services 
                WHERE name = ?
            """, (service_name,))
            price = cursor.fetchone()
            prices.append(price[0] if price else 'N/A')
        # Check in the table of professional
        cursor.execute("""SELECT * FROM professional WHERE username=? AND password=?""", (username, password))
        user2 = cursor.fetchone()
        cursor.execute("""SELECT id, cust_name, cust_phone
            FROM service_history 
            WHERE service_name = (SELECT service_name FROM professional WHERE username=?) 
            AND status='OPEN'
        """, (username,))
        service_user2=cursor.fetchall()
        db.close()

        if user1:
            session['name'] = user1[1]
            session['username'] = user1[0]
            return render_template('user_page.html', name=user1[1], service_history=service_user1,prices=prices,zip=zip)
        elif user2:
            session['name'] = user2[1]
            session['username'] = user2[0]
            return render_template('professional_page.html', name=user2[1], service_history=service_user2)
        else:
            return render_template('login.html', message='Invalid credentials, please try again.')
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def cust_signup():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        gender = request.form['gender']
        address = request.form['address']
        city = request.form['city']
        phone = request.form['phone']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("""INSERT INTO customer (username, name, gender, address, city, phone, password) VALUES (?, ?, ?, ?, ?, ?, ?)""", 
                       (username, name, gender, address, city, phone, password))
        db.commit()
        db.close()

        return redirect(url_for('login_details'))
    return render_template('signup.html')

@app.route('/service_signup', methods=['POST', 'GET'])
def prof_signup():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        gender = request.form['gender']
        address = request.form['address']
        city = request.form['city']
        phone = request.form['phone']
        password = request.form['password']
        service = request.form['service']
        yoe = request.form['yoe']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("""INSERT INTO professional (username, name, gender, address, city, phone, password, experience, service_name) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                       (username, name, gender, address, city, phone, password, yoe, service))
        db.commit()
        db.close()

        return redirect(url_for('login_details'))
    return render_template('service_signup.html')

@app.route('/user_page', methods=['GET'])
def user_page():
    if 'username' in session:
        username = session['username']
        name = session['name']
        db = get_db()
        cursor = db.cursor()

        # Fetch user's service history
        cursor.execute("""
            SELECT service_name, Prof_name, Prof_phone, status, id 
            FROM service_history 
            WHERE username = ?
        """, (username,))
        service_history = cursor.fetchall()

        # Fetch prices for each service in the history
        prices = []
        for history in service_history:
            service_name = history[0]
            cursor.execute("""
                SELECT price 
                FROM services 
                WHERE name = ?
            """, (service_name,))
            price = cursor.fetchone()
            prices.append(price[0] if price else 'N/A')

        db.close()

        return render_template('user_page.html', name=name, service_history=service_history, prices=prices,zip=zip)
    return redirect(url_for('login_details'))


@app.route('/user_page/booking_page_appliance', methods=['GET','POST'])
def appliance():
    if 'username' in session:
        if request.method=='POST':
            username = session['username']
            db = get_db()
            cursor = db.cursor()
            cursor.execute("""INSERT INTO service_history (username, service_name, status, cust_name, cust_phone)
                                SELECT ?, 'Appliance Repairing', 'OPEN', name, phone FROM customer WHERE username = ?;
                                """, (username,username))
            db.commit()
            db.close()
            flash('Booking successful, our professional will get in touch shortly.')
            return redirect(url_for('user_page'))
        else:
            name=session['name']
            return render_template('booking_page_appliance.html',name=name)
    else:
        flash('Booking failed due to some technical reasons.')
        return redirect(url_for('user_page'))

@app.route('/user_page/booking_page_home_cleaning', methods=['GET','POST'])
def home_cleaning():
    if 'username' in session:
        if request.method=='POST':
            username = session['username']
            db = get_db()
            cursor = db.cursor()
            cursor.execute("""INSERT INTO service_history (username, service_name, status, cust_name, cust_phone)
                                SELECT ?, 'Home Cleaning', 'OPEN', name, phone FROM customer WHERE username = ?;
                                """, (username,username))
            db.commit()
            db.close()
            flash('Booking successful, our professional will get in touch shortly.')
            return redirect(url_for('user_page'))
        else:
            name=session['name']
            return render_template('booking_page_home_cleaning.html',name=name)
    else:
        flash('Booking failed due to some technical reasons.')
        return redirect(url_for('login_details'))

@app.route('/user_page/booking_page_beauty_wellness', methods=['GET','POST'])
def beauty_wellness():
    if 'username' in session:
        if request.method=='POST':
            username = session['username']
            db = get_db()
            cursor = db.cursor()
            cursor.execute("""INSERT INTO service_history (username, service_name, status, cust_name, cust_phone)
                                SELECT ?, 'Beauty and Wellness', 'OPEN', name, phone FROM customer WHERE username = ?;
                                """, (username,username))
            db.commit()
            db.close()
            flash('Booking successful, our professional will get in touch shortly.')
            return redirect(url_for('user_page'))
        else:
            name=session['name']
            return render_template('booking_page_beauty_wellness.html',name=name)
    else:
        flash('Booking failed due to some technical reasons.')
        return redirect(url_for('login_details'))

@app.route('/user_page/booking_page_pest_control', methods=['GET','POST'])
def pest_control():
    if 'username' in session:
        if request.method=='POST':
            username = session['username']
            db = get_db()
            cursor = db.cursor()
            cursor.execute("""INSERT INTO service_history (username, service_name, status, cust_name, cust_phone)
                                SELECT ?, 'Pest Control', 'OPEN', name, phone FROM customer WHERE username = ?;
                                """, (username,username))
            db.commit()
            db.close()
            flash('Booking successful, our professional will get in touch shortly.')
            return redirect(url_for('user_page'))
        else:
            name=session['name']
            return render_template('booking_page_pest_control.html',name=name)
    else:
        flash('Booking failed due to some technical reasons.')
        return redirect(url_for('login_details'))

@app.route('/user_page/booking_page_gardening', methods=['GET','POST'])
def gardening():
    if 'username' in session:
        if request.method=='POST':
            username = session['username']
            db = get_db()
            cursor = db.cursor()
            cursor.execute("""INSERT INTO service_history (username, service_name, status, cust_name, cust_phone)
                                SELECT ?, 'Gardening', 'OPEN', name, phone FROM customer WHERE username = ?;
                                """, (username,username))
           
            db.commit()
            db.close()
            flash('Booking successful, our professional will get in touch shortly.')
            return redirect(url_for('user_page'))
        else:
            name=session['name']
            return render_template('booking_page_gardening.html',name=name)
    else:
        flash('Booking failed due to some technical reasons.')
        return redirect(url_for('login_details'))

@app.route('/user_page/cancel/<int:id>',methods=['GET','POST'])
def cancel(id):
    if 'username' in session:
        if request.method=='POST':
            db=get_db()
            cursor=db.cursor()
            cursor.execute("""delete from service_history where id=?""",(id,))
            db.commit()
            db.close()
            flash("Your booking is deleted")
            return redirect(url_for('user_page'))
        else:
            name=session['name']
            return render_template('cancel_page.html',name=name, id=id)

    else:
        flash("Not possible")
        return redirect(url_for('login_details'))

@app.route('/user_page/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    if 'username' in session:
        if request.method=='POST':
            service=request.form['service_name']
            db=get_db()
            cursor=db.cursor()
            cursor.execute("""update service_history set service_name=? where id=?""",(service,id))
            db.commit()
            db.close()
            flash('Booking edited successfully')
            return redirect(url_for('user_page'))
        else:
            name=session['name']
            return render_template('edit_page.html',name=name,id=id)
    else:
        flash("You need to login again")
        return redirect(url_for('login_details'))  

@app.route('/user_page/profile', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        username = session['username']
        db = get_db()
        cursor = db.cursor()
        
        if request.method == 'POST':
            new_name = request.form.get('name')
            new_address = request.form.get('address')
            new_phone = request.form.get('phone')
            
            cursor.execute("""
                UPDATE customer 
                SET name = ?, address = ?, phone = ? 
                WHERE username = ?
            """, (new_name, new_address, new_phone,username ))
            db.commit()
            db.close()
            flash('Profile updated successfully.')
            return redirect(url_for('user_page'))

        cursor.execute("SELECT name, address, phone FROM customer WHERE username = ?", (username,))
        user_details = cursor.fetchone()
        db.close()

        return render_template('user_prof.html', user_details=user_details)
    return redirect(url_for('login_details'))

@app.route('/user_page/user_summary')
def user_summary():
    if 'username' in session:
        db = get_db()
        cursor = db.cursor()

        username = session['username']

        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM service_history
            WHERE username = ?
            GROUP BY status
        """, (username,))
        data = cursor.fetchall()
        
        labels = [row[0] for row in data]
        values = [row[1] for row in data]

        db.close()

        return render_template('user_summary.html', labels=labels, values=values)
    return redirect(url_for('login_details'))



@app.route('/professional_page', methods=['GET'])
def prof_page():
    if 'username' in session:
        name = session['name']
        username=session['username']
        db=get_db()
        cursor=db.cursor()
        cursor.execute("""
            SELECT id, cust_name, cust_phone
            FROM service_history 
            WHERE service_name = (SELECT service_name FROM professional WHERE username=?) 
            AND status='OPEN'
        """, (username,))
        history=cursor.fetchall()
        print("Fetched History:",history)
        db.close()
        return render_template('professional_page.html', name=name ,service_history=history)
    return redirect(url_for('login_details'))

@app.route('/professional_page/professional_profile', methods=['GET', 'POST'])
def professional_profile():
    if 'username' in session:
        username = session['username']
        db = get_db()
        cursor = db.cursor()
        
        if request.method == 'POST':
            new_name = request.form.get('name')
            new_phone = request.form.get('phone')
            new_service_name = request.form.get('service_name')
            new_experience = request.form.get('experience')

            cursor.execute("""
                UPDATE professional 
                SET name = ?, phone = ?, service_name = ?, experience = ? 
                WHERE username = ?
            """, (new_name, new_phone, new_service_name, new_experience, username))
            db.commit()
            db.close()
            flash('Profile updated successfully.')
            return redirect(url_for('prof_page'))

        cursor.execute("SELECT name, phone, service_name, experience FROM professional WHERE username = ?", (username,))
        professional_details = cursor.fetchone()
        db.close()

        return render_template('professional_profile.html', professional_details=professional_details)
    return redirect(url_for('login'))


@app.route('/professional_page/accept/<int:id>',methods=['POST'])
def accept(id):
    if 'username' in session:
        username=session['username']
        db=get_db()
        cursor=db.cursor()
        cursor.execute("""
            UPDATE service_history SET Prof_name = (SELECT name FROM professional WHERE username = ?), Prof_phone = (SELECT phone FROM professional WHERE username = ?), status = 'ASSIGNED' WHERE id = ? """, (username, username, id)
        )
        db.commit()
        db.close()
        flash("Accepted")
        return redirect(url_for('prof_page'))
    return redirect(url_for('login_details')) 

@app.route('/professional_page/reject/<int:id>', methods=['POST'])
def reject(id):
    if 'username' in session:
        username = session['username']
        db = get_db()
        cursor = db.cursor()

        # Update the status to 'REJECTED'
        cursor.execute("""
            UPDATE service_history 
            SET status = 'REJECTED' 
            WHERE id = ? 
            AND service_name = (SELECT service_name FROM professional WHERE username = ?)
        """, (id, username))
        
        db.commit()
        db.close()
        flash('Request has been rejected and removed from your dashboard.')
        return redirect(url_for('prof_page'))
    else:
        flash("You need to login again.")
        return redirect(url_for('login_details'))

@app.route('/professional_page/close_request/<int:id>', methods=['POST'])
def close_request(id):
    if 'username' in session:
        username = session['username']
        db = get_db()
        cursor = db.cursor()

        # Update the status to 'CLOSED'
        cursor.execute("""
            UPDATE service_history 
            SET status = 'CLOSED' 
            WHERE id = ? 
            AND service_name = (SELECT service_name FROM professional WHERE username = ?)
        """, (id, username))
        
        db.commit()
        db.close()
        flash('Request has been closed.')
        return redirect(url_for('accepted_requests'))
    else:
        flash("You need to login again.")
        return redirect(url_for('login_details'))

@app.route('/professional_page/accepted_requests', methods=['GET'])
def accepted_requests():
    if 'username' in session:
        name = session['name']
        username = session['username']
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT id, cust_name, cust_phone 
            FROM service_history 
            WHERE service_name = (SELECT service_name FROM professional WHERE username=?) 
            AND status = 'ASSIGNED'
        """, (username,))
        accepted_history = cursor.fetchall()
        db.close()

        return render_template('prof_accepted.html', name=name, accepted_history=accepted_history)
    return redirect(url_for('login_details'))

@app.route('/professional_page/professional_summary')
def professional_summary():
    if 'username' in session:
        db = get_db()
        cursor = db.cursor()

        username = session['username']
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM service_history
            WHERE prof_name = (SELECT name FROM professional WHERE username = ?)
            GROUP BY status
        """, (username,))
        data = cursor.fetchall()
        
        labels = [row[0] for row in data]
        values = [row[1] for row in data]

        db.close()

        return render_template('professional_summary.html', labels=labels, values=values)
    return redirect(url_for('login_details'))


@app.route('/admin_active_requests', methods=['GET'])
def admin_active_requests():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, service_name, cust_name, cust_phone, Prof_name, Prof_phone, status 
        FROM service_history 
    """)
    active_requests = cursor.fetchall()
    db.close()

    return render_template('admin_page.html', active_requests=active_requests)
    

@app.route('/prof_data', methods=['GET'])
def prof_data():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT name, phone, username, experience, service_name, gender ,rating
        FROM professional
    """)
    professionals = cursor.fetchall()
    db.close()

    return render_template('prof_data.html', professionals=professionals)


@app.route('/remove_prof/<string:username>', methods=['POST'])
def remove_prof(username):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT phone FROM professional WHERE username = ?", (username,))
    prof_phone = cursor.fetchone()

    if prof_phone:
        prof_phone = prof_phone[0]

        cursor.execute("DELETE FROM professional WHERE username = ?", (username,))
        
        cursor.execute("""
            UPDATE service_history 
            SET status = 'OPEN', Prof_name = NULL, Prof_phone = NULL 
            WHERE Prof_phone = ?
        """, (prof_phone,))

        db.commit()
        flash('Professional has been removed and corresponding services have been updated.')
        
    else:
        flash('Professional not found.')

    db.close()
    return redirect(url_for('prof_data'))
    

@app.route('/logout') 
def logout(): 
    session.pop('username', None) 
    session.pop('name', None) 
    return redirect(url_for('login_details'))

@app.route('/admin_active_requests/manage',methods=['GET'])
def price():
    if request.method=='GET':
        db=get_db()
        cursor=db.cursor()
        cursor.execute("""select * from services""")
        services=cursor.fetchall()
        db.close()
        return render_template('prices.html',services=services)
    
@app.route('/admin_active_requests/update_price/<string:service_name>', methods=['POST'])
def update_price(service_name):
    new_price = request.form.get('new_price')
    
    if new_price:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE services 
            SET price = ? 
            WHERE name = ?
        """, (new_price, service_name))
        
        db.commit()
        db.close()
        flash('Price updated successfully.')
        return redirect(url_for('price'))
    else:
        flash('Please provide a new price.')
        return redirect(url_for('price'))
    
@app.route('/add_service', methods=['POST'])
def add_service():
    if 'username' in session:
        service_name = request.form.get('service_name')
        service_price = request.form.get('service_price')
        
        if service_name and service_price:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO services (name, price) 
                VALUES (?, ?)
            """, (service_name, service_price))
            
            db.commit()
            db.close()
            flash('Service added successfully.')
        else:
            flash('Please provide both service name and price.')
        
        return redirect(url_for('price'))
    return redirect(url_for('login_details'))

@app.route('/delete_service/<service_name>', methods=['POST']) 
def delete_service(service_name): 
    db = get_db() 
    cursor = db.cursor() 
    cursor.execute("DELETE FROM services WHERE name = ?", (service_name,)) 
    db.commit() 
    db.close() 
    flash('Service deleted successfully.') 
    return redirect(url_for('price'))

@app.route('/admin_summary')
def admin_summary():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM service_history
        GROUP BY status
    """)
    data = cursor.fetchall()
    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    db.close()
    return render_template('admin_summary.html', labels=labels, values=values)



@app.route('/rate/<int:prof_id>', methods=['GET', 'POST'])
def rate_professional(prof_id):
    if 'username' in session:
        db = get_db()
        cursor = db.cursor()

        if request.method == 'POST':
            rating = request.form.get('rating')

            if rating:
                # Update the professional's rating
                cursor.execute("""
                    UPDATE professional 
                    SET rating = ? 
                    WHERE phone = ?
                """, (rating, prof_id))

                db.commit()
                db.close()
                flash('Your rating and review have been submitted.')
                return redirect(url_for('user_page')) 
            else:
                flash('Please provide a rating.')
                return redirect(url_for('user_page'))

        cursor.execute("SELECT name, phone FROM professional WHERE phone = ?", (prof_id,))
        prof_details = cursor.fetchone()
        db.close()

        return render_template('rate.html', prof_details=prof_details)
    return redirect(url_for('login_details'))


if __name__ == '__main__':
    app.run(debug=True)
