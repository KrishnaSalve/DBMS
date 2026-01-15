from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)


class User(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()


@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']

        new_user = User(
            username = username,
            password = password
        )
        db.session.add(new_user)
        db.session.commit()
    return render_template('index.html')


@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        sno = request.form['sno']
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(sno = sno).first()
        if user:
            user.username = username 
            user.password = password

        db.session.add(user)
        db.session.commit()
    return render_template('update.html')


@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    if request.method == 'POST':
        sno = request.form['sno']

        user = User.query.filter_by(sno = sno).first()
        if user:
            db.session.delete(user)
            db.session.commit()

    return render_template('delete.html')


@app.route('/database')
def database():
    users = User.query.all()
    print(users)
    return render_template("database.html", users=users)



if __name__ == "__main__":
    app.run(debug=True)