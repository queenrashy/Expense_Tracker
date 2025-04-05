from flask import jsonify, request
from app import app, db
from datetime import datetime
from models import Expenses, TotalBudget
from auth import auth

# Add to expenses
@app.route('/add-expenses', methods=['POST'])
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
    
    # Create new expense
    new_expenses = Expenses(category=category, budget=budget, start_date=new_start_date, end_date=new_end_date, user_id=current_user.id)
    db.session.add(new_expenses)
    db.session.commit()
    
    # Calculate time periods for budget allocation
    today = datetime.now()
    delta_days = (new_end_date - new_start_date).days
    
    # calculate budget allocations based on time period
    # divide the budget by the number of days and multiply by period length and add 1 to avoid division by zero
    daily_budget = float(budget) / max(delta_days, 1)
    
    weekly_allocation = daily_budget * 7
    monthly_allocation = daily_budget * 30
    three_month_allocation = daily_budget * 90
    
    # Update total budget for the user
    # First check if user already has a total budget record
    total_budget = TotalBudget.query.filter_by(user_id=current_user.id).first()
    
    if total_budget:
        # Update existing total budget
        total_budget.monthly_budget = total_budget.monthly_budget + float(budget) if total_budget.monthly_budget else float(budget)
        # total budget in  week
        total_budget.Total_in_week = total_budget.Total_in_week + weekly_allocation if total_budget.Total_in_week else weekly_allocation
        
        # total budget in a month
        total_budget.Total_in_month = total_budget.Total_in_Month + monthly_allocation if total_budget.Total_in_Month else monthly_allocation
        # total budget in 3months
        total_budget.Total_in_3months = total_budget.Total_in_3months + three_month_allocation if total_budget.Total_in_week else three_month_allocation
    else:
        # Create new total budget record
        new_total_budget = TotalBudget(
            user_id=current_user.id,
            monthly_budget=float(budget),
            Total_in_week=weekly_allocation,
            Total_in_Month=monthly_allocation,
            Total_in_3months=three_month_allocation
        )
        db.session.add(new_total_budget)
    
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

# delete category
@app.route('/<int:id>', methods=['DELETE'])
@auth.login_required  
def delete_category_id(id):
    expenses = Expenses.query.filter(Expenses.id == id).first()
    
    if expenses is None:
        return jsonify({'erorr': 'expenses doe not  exist'}), 404
    
    db.session.delete(expenses)
    db.session.commit()
    return jsonify({'done': True, 'message': f'{expenses.category} Account deleted successfully!'}), 201
  