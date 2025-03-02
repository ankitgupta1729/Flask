from flask import Flask, request, jsonify,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ankit135@localhost:5432/flask_database'

db=SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    pet = db.Column(db.String(100))

    def __init__(self, fname, lname, pet):
        self.fname = fname
        self.lname = lname
        self.pet = pet

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET','POST'])
def submit():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        pet = request.form['pets']
        student=Student(fname,lname,pet)
        db.session.add(student)
        db.session.commit()
        
        #if request.method=='GET':
        # fetch a cretain student record
        studentResult=db.session.query(Student).filter(Student.id==1)
        for result in studentResult:
            print(result.fname)
        
        return render_template('success.html',data=fname)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)