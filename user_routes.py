from flask import jsonify, request
from app import app, db
from models import User
from toolz import is_valid_email
from auth import auth

@app.route('/signup', methods=['POST'])
def sign_up():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # if username form is empty or less than 2
    if username is None or len(username) < 2 :
        return jsonify({'error': 'Please enter a valid name'}), 404
    
    # check if user exist
    exist = User.query.filter(User.username == username).first()
    if exist is not None:
        return jsonify({'error': 'username already exists'}), 404
    
    # verify is email is real
    if not is_valid_email(email):
        return jsonify({'error': 'Enter a valid email'}), 404
    
    # check if email already exist
    exist = User.query.filter(User.email == email).first()
    if exist is not None:
        return jsonify({'error': 'Email already exists'}), 400
    
    # if password form is empty or less than 6
    if password is None or len(password) < 6:
        return jsonify({'error': 'Please enter 6 or more characters'})
    
    # add new user
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    new_user.set_password(password)
    
    try:
        db.session.commit()
        return jsonify({'done': True, 'Created': 'Account successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'User signup error: {e}'}), 400   
    
    

@app.route('/login')
def login_user():
    email = request.json.get('email')
    password = request.json.get('password')
    
    if email is None or password is None:
        return jsonify({'error': 'Please enter a valid email and password.'}), 401
    
    if not is_valid_email(email):
        return jsonify({'error': 'Please enter a valid email address!'}), 400
    
    # find user
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({'error': 'User with this email does not exist'}), 401
    
    # validate password
    if user.check_password(password):
        # password is correct, generate jwt token
        token = user.generate_auth_token()
        return jsonify({'success': True, 'token': token}), 200
    
    return jsonify({'error': 'Invalid email or password.'})


# update username or email
@app.route('/<int:id>', methods=['PUT'])
@auth.login_required  
def update_user(id):
    user = User.query.filter(User.id == id).one_or_404()
    data = request.json
    user.username = data.get('username') or user.username
    user.email = data.get('email') or user.email
    user.password = data.get('password') or user.password
    
   
    
    # error if user don't change username
    exist = User.query.filter(User.username == data.get('username'), User.id != id).first()
    if exist is not None:
        return jsonify({'error': "Username already taken. Choose a different one."}), 404
    
    # error if user don't change email
    exist = User.query.filter(User.email == data.get('email'), User.id !=id).first()
    if exist is not None:
        return jsonify({'error': "email already taken. Choose a different one."})
    
    if user:
        db.session.commit()
        return jsonify({'done': True, 'message': f'user {user.username} updated successfully'}), 200


@app.route('/<int:id>', methods=['DELETE'])
@auth.login_required  
def delete_account(id):
    user = User.query.filter(User.id == id).first()
    
    if user is None:
        return jsonify({'error': 'User does not exist'}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'done': True, 'message': f'{user.username} Account deleted successfully!'}), 200
    
    
# get user profile
@app.route('/profile', methods=['GET'])
@auth.login_required  
def profile():
    current_user = auth.current_user()
    return jsonify(current_user.as_dict())

# get user budget
@app.route('/get-expenses')
@auth.login_required  
def expenses():
    current_user = auth.current_user()
    user_expense = current_user.expenses
    expenses = []
    for expense in user_expense:
       expenses.append({
            "id": expense.id,
            "category":expense.category,
            "budget": expense.budget,
            "start_date": expense.start_date,
            "end_date": expense.end_date
        })

    return jsonify({'expenses':expenses})