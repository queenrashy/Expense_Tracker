from flask import jsonify, request
from app import app, db
from datetime import datetime
from models import Budget
from auth import auth


@app.route('/add-budget', methods=['POST'])
@auth.login_required  
def add_budget():
    current_user = auth.current_user()
    data = request.json
    expenses_type = data.get('expenses_type')
    category = data.get('category')
    description = data.get('description')
    date = data.get('date')
    marchant = data.get('marchant')
    amount = data.get('amount')
    
    if not expenses_type or not category or not description or not date or not marchant or not amount:
        return jsonify({'error': 'All field required'}), 400
    try:
        budget_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    try:
        amount = float(data.get('amount'))
    except ValueError:
        return  jsonify({'error': 'Amount must be a valid number'}), 400
    
    new_budget = Budget(expenses_type=expenses_type, category=category, description=description, date = budget_date, marchant=marchant, amount=amount, expenses_id= current_user.id )
    db.session.add(new_budget)
    db.session.commit()
    return jsonify({'done':True, 'message': 'Budget added successfully'}), 201

# delete budget
@app.route('/budget/<int:id>', methods=['DELETE'])
@auth.login_required  
def delete_budget_id(id):
    budget = Budget.query.filter(Budget.id == id).first()
    
    if budget is None:
        return jsonify({'error': 'Budget does not exist'}), 404
    
    db.session.delete(budget)
    db.session.commit()
    return jsonify({'done': True, 'message': f'{budget.expenses_type} deleted '}), 200
    
