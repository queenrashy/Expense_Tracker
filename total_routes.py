from flask import jsonify, request
from app import app, db
from datetime import datetime
from models import TotalBudget, Expenses, Budget
from auth import auth




# @app.route('/add-expenses', methods=['POST'])
@auth.login_required  
def add_expenses():
    current_user = auth.current_user()
    data = request.json
    category = data.get('category')
    budget = data.get('budget')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    # check if user field all form
    if not category  or  not budget or  not start_date or not end_date :
        return jsonify({'error': 'All fields required'})
    
    # check if category already exists
    existing_expense = Expenses.query.filter_by(category=category).first()
    if existing_expense:
        return jsonify({'error': 'Category already exists. Choose a different category'})
    
    # change start_date to be in date format
    try:
        new_start_date = datetime.strptime(start_date, "%Y-%m-%d")
        new_end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}),400
    
    
    
    new_expenses = Expenses(category=category, budget=budget, start_date=new_start_date, end_date=new_end_date, user_id=current_user.id)
    db.session.add(new_expenses)
    db.session.commit()
    return jsonify({'done': True, 'message': 'Expense added successfully'}), 200



# update expenses
@app.route('/category/<int:id>', methods=['PUT'])
@auth.login_required  
def update_category(id):
    existing_category = Expenses.query.filter_by(id=id).first()
    
    if not existing_category:
        return jsonify({'error': 'Category not found.'}), 404
    
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # update category and check if it already exists before updating
    if 'category' in data:
        duplicate_category = Expenses.query.filter(
            Expenses.category == data.get('category'),
            Expenses.id == id
        ).first()
        # Check if the category already exists 
        if duplicate_category:
            return jsonify({'error': 'Category already exists. Please use a different category.'}), 400
        
        existing_category.category = data['category']
    
    # Update budget 
    if 'budget' in data:
        existing_category.budget = data['budget']
    
    db.session.commit()
    return jsonify({'done': True, 'message': 'Updated successfully'}), 200