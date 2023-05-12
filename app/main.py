from flask_login import login_required, login_user, logout_user
from flask import request,jsonify,session
from settings import app,db,cache,login_manager
from models import User,Student
import json
import time

# Curent User Loader

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Sign up

@app.route('/signup', methods=['POST'])
def signup():
    username=request.form.get('username') or request.get_json()['username']
    password=request.form.get('password') or request.get_json()['password']
    if not username or not password:
        return jsonify({'error': 'Missing fields, Kindly provide both username & password.'}), 400
    user=User(username=username,password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"success":"new user has been created."}), 201

# Login 

@app.route('/login',methods=['POST'])
def login():
    username=request.form.get('username') or request.get_json()['username']
    password=request.form.get('password') or request.get_json()['password']
    if not username or not password:
        return jsonify({'error': 'Missing fields, Kindly provide both username & password.'}), 400
    user= User.query.filter_by(username=username,password=password).first()
    if user:
        login_user(user)
        return jsonify({'success': 'User authenticated sucessfully.'}), 200
    else:
        return jsonify({'error': 'Invalid username or password.'}), 401
        
# Log-out 

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'success': 'User sucessfully logged out.'}), 200

# Rate Limiter function 

def rate_limiter(key):
    current_time=time.time()
    if cache.get(key):
        last_time=float(cache.get(key))
        if current_time - last_time < app.config['RATE_LIMIT_EXPIRE']:
            return True
    cache.set(key,current_time)
    return False

# Create student 

@app.route('/student/create',methods=['POST'])
@login_required
def create_student():
    if rate_limiter('create_student'):
        return jsonify({'error': "Too many requests. Only one request per minute."}), 429 
    name=request.form.get('name') or request.get_json()['name']
    age=request.form.get('age') or request.get_json()['age']
    standard=request.form.get('standard') or request.get_json()['standard']
    rollnumber=request.form.get('rollnumber') or request.get_json()['rollnumber']

    if not name or not age or not standard or not rollnumber:
        return jsonify({'error': 'Missing fields'}), 400
    
    student=Student(name=name, age=age, standard=standard,rollnumber=rollnumber)
    db.session.add(student)
    db.session.commit()
    cache.delete('students')
    return jsonify(student.show()), 201

# Get single student By ID

@app.route('/student/<int:id>')
@login_required
def get_student(id):
    if rate_limiter(f'get_student:{id}'):
        return jsonify({'error': "Too many requests. Only one request per minute."}), 429
    student=cache.get(f'student:{id}')
    if student:
        student_dict=json.loads(student)
        print("fetching from cache")
        return jsonify(student_dict), 200
    else:
        student=db.session.get(Student, id)
        if student:
            student_dict=student.show()
            cache.set(f'student:{id}',json.dumps(student_dict))
            print("fetching from DB")
            return jsonify(student_dict), 200
        else:
            return jsonify({'error': f"Student ID ({id}) doesn't exist"}), 404
        
# Get all students

@app.route('/students')
@login_required
def get_students():
    if rate_limiter('get_students'):
        return jsonify({'error': "Too many requests. Only one request per minute."}), 429
    students=cache.get('students')
    if students:
        students=json.loads(students)
        print("fetching from cache")
        return jsonify(students),200
    else:
        students=[student.show() for student in db.session.query(Student).all()]
        if len(students)>0:
            cache.set('students',json.dumps(students))
            print("fetching from DB")
            return jsonify(students),200
        else:
            return jsonify({'error': "There are no student record yet so far. Kindly create new student."}), 404


# Run the application
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
