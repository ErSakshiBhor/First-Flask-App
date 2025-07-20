from flask import Flask, render_template, request, flash, redirect, url_for 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime   


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"

db = SQLAlchemy(app)

# to define columns
class User(db.Model):   
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(567), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    
# to create database
with app.app_context():
    db.create_all()

app.secret_key = "your_secret_key_here"  # Required for flash messages

# to create routes(paths)
@app.route('/')
def home():
    all_users = User.query.all()
    return render_template('index.html', all_users = all_users)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods = ["GET",'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(
            username = username,
            password = password
        )
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Error: This username already exists. Please try another email.", "danger")
            return redirect(url_for('register'))  # Redirect to clear flash message after refresh
        
        # If user does not exist, add them
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        #to confirm
        db.session.commit()
       
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('register'))  # Redirect to clear flash message
    
    return render_template('register.html')

@app.route('/update/<sno>', methods = ["GET",'POST'])
def update(sno):
    user = User.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user.username = username
        user.password = password
        # to update data into database
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('update.html', user = user)

@app.route('/delete/<sno>', methods = ["GET",'POST'])
def delete(sno):
    user = User.query.filter_by(sno=sno).first()
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

@app.route('/login', methods = ["GET",'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
           
            return redirect(url_for('home'))  # Redirect to homepage after successful login
            # flash("Login successful!", "success")
        else:
            flash("Invalid username or password. Please try again.", "danger")
    
    return render_template('login.html')

if __name__ == "__main__":  
    app.run(debug=True)