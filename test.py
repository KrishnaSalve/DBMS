from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import base64


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


db = SQLAlchemy(app)

class USER(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    Occupation = db.Column(db.String(200), nullable=False)
    Image = db.Column(db.LargeBinary, nullable=True)

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['email']
        occupation= request.form['password']
        image = request.files['image'].read()
        
        new_user = USER(
            Name = name,
            Occupation = occupation,
            Image = image
        )

        db.session.add(new_user)
        db.session.commit()
    return render_template('start.html')


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        srno = request.form['srno']
        name = request.form['email']
        occupation = request.form['password']

        user = USER.query.filter_by(srno = srno).first()
        if user:
            user.Name = name
            user.Occupation = occupation

        db.session.add(user)
        db.session.commit()
    return render_template('update.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        srno = request.form['srno']

        user = USER.query.filter_by(srno = srno).first()
        if user:
            db.session.delete(user)
            db.session.commit()
        
    return render_template('delete.html')


@app.route('/database')
def database():
    users = USER.query.all()
    
    image_list = []
    for u in users:
        if u.Image:
            image_list.append(base64.b64encode(u.Image).decode('ascii'))
        else:
            image_list.append(None)

    return render_template('database.html', users = users, images = image_list)
    

if __name__ == "__main__":
    app.run(debug=True)
