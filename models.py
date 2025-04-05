import os
import jwt
from app import db
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=True, unique=True)
    email = db.Column(db.String(200), nullable=True, unique=True)
    password_hash = db.Column(db.String(100))
    create = db.Column(db.DateTime, default=datetime.now)
    expenses = relationship("Expenses", back_populates="user")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __repr__(self):
        return f"<User {self.id}>"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_auth_token(self):
        expiration_time = datetime.now() + timedelta(days=10)
        payload = {
            'id' : self.id,
            'exp' : expiration_time,
        }
        token = jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm='HS256')
        return token
        
    @staticmethod
    def verify_auth_token(token):
        if not token:
            return None
        try:
            payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
            user = User.query.get(payload['id'])
            return user
        except jwt.ExpiredSignatureError:
            print("Token has expired ")
            return None
        except jwt.DecodeError:
            print("Token is invalid")
            return None
            
            
# Actual budget in a month or year
class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.Column(db.String(200), unique=True)
    budget = db.Column(db.Float)
    start_date = db.Column(db.DateTime, default=datetime.now)
    end_date = db.Column(db.DateTime)
    
    user = relationship("User", back_populates="expenses")
    budgets = relationship("Budget", back_populates="expenses")  

    def __repr__(self):
        return f"<Expenses {self.id}>"
    
    
# Type of budget and descriptions
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expenses_id = db.Column(db.Integer, db.ForeignKey('expenses.id'))
    expenses_type = db.Column(db.String(400))
    category = db.Column(db.String(200))
    description = db.Column(db.String(500))
    date = db.Column(db.DateTime, default=datetime.now)
    marchant = db.Column(db.String(300))
    amount = db.Column(db.Integer)
    expenses = relationship("Expenses", back_populates="budgets")  
    total_budget = relationship("TotalBudget", back_populates="budget")  #

    def __repr__(self):
        return f'<Budget {self.id}>'
    
    

# Monthly budget
class TotalBudget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'))
    monthly_budget = db.Column(db.Integer)
    Total_in_week = db.Column(db.Integer)
    Total_in_Month = db.Column(db.Integer)
    Total_in_3months = db.Column(db.Integer)
    budget = relationship("Budget", back_populates="total_budget")
    def __repr__(self):
        return f"<TotalBudget {self.id}>"
