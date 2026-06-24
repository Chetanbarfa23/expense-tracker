from flask import Blueprint, request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from extensions import db
from models.expense_model import Expense

import traceback

# =====================================
# BLUEPRINT
# =====================================

expense = Blueprint(
    'expense',
    __name__
)

# =====================================
# ALLOWED CATEGORIES
# =====================================

ALLOWED_CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Bills",
    "Entertainment",
    "Healthcare",
    "Education",
    "Other"
]

# =====================================
# ADD EXPENSE
# =====================================

@expense.route(
    '/add-expense',
    methods=['POST']
)
@jwt_required()

def add_expense():

    try:

        # GET USER ID FROM JWT
        user_id = int(get_jwt_identity())

        # GET REQUEST DATA
        data = request.get_json()

        if not data:

            return {
                "success": False,
                "message": "No data provided"
            }, 400

        amount = data.get('amount')
        category = data.get('category')
        description = data.get(
            'description',
            ''
        )

        # VALIDATION
        if amount is None:

            return {
                "success": False,
                "message": "Amount is required"
            }, 400

        try:

            amount = float(amount)

        except Exception:

            return {
                "success": False,
                "message": "Amount must be a number"
            }, 400

        if amount <= 0:

            return {
                "success": False,
                "message": "Amount must be positive"
            }, 400

        if category not in ALLOWED_CATEGORIES:

            return {
                "success": False,
                "message": f"Category must be one of {ALLOWED_CATEGORIES}"
            }, 400

        # CREATE EXPENSE
        new_expense = Expense(
            amount=amount,
            category=category,
            description=description,
            user_id=user_id
        )

        db.session.add(new_expense)

        db.session.commit()

        return {
            "success": True,
            "message": "Expense added successfully",
            "expense": {
                "id": new_expense.id,
                "amount": new_expense.amount,
                "category": new_expense.category,
                "description": new_expense.description,
                "user_id": new_expense.user_id,
                "created_at": str(
                    new_expense.created_at
                ) if new_expense.created_at else None
            }
        }, 201

    except Exception as e:

        traceback.print_exc()

        db.session.rollback()

        return {
            "success": False,
            "error": str(e)
        }, 500


# =====================================
# GET ALL EXPENSES
# =====================================

@expense.route(
    '/expenses',
    methods=['GET']
)
@jwt_required()

def get_expenses():

    try:

        user_id = int(get_jwt_identity())

        expenses = Expense.query.filter_by(
            user_id=user_id
        ).all()

        expense_list = []

        for expense_data in expenses:

            expense_list.append({

                "id":
                    expense_data.id,

                "amount":
                    float(expense_data.amount),

                "category":
                    expense_data.category,

                "description":
                    expense_data.description,

                "user_id":
                    expense_data.user_id,

                "created_at":
                    str(expense_data.created_at)
                    if expense_data.created_at
                    else None
            })

        return {
            "success": True,
            "count": len(expense_list),
            "expenses": expense_list
        }, 200

    except Exception as e:

        traceback.print_exc()

        return {
            "success": False,
            "error": str(e)
        }, 500


# =====================================
# DELETE EXPENSE
# =====================================

@expense.route(
    '/expense/<int:id>',
    methods=['DELETE']
)
@jwt_required()

def delete_expense(id):

    try:

        user_id = int(get_jwt_identity())

        expense_data = Expense.query.filter_by(
            id=id,
            user_id=user_id
        ).first()

        if not expense_data:

            return {
                "success": False,
                "message": "Expense not found"
            }, 404

        db.session.delete(expense_data)

        db.session.commit()

        return {
            "success": True,
            "message": "Expense deleted successfully"
        }, 200

    except Exception as e:

        traceback.print_exc()

        db.session.rollback()

        return {
            "success": False,
            "error": str(e)
        }, 500


# =====================================
# UPDATE EXPENSE
# =====================================

@expense.route(
    '/expense/<int:id>',
    methods=['PUT']
)
@jwt_required()

def update_expense(id):

    try:

        user_id = int(get_jwt_identity())

        data = request.get_json()

        expense_data = Expense.query.filter_by(
            id=id,
            user_id=user_id
        ).first()

        if not expense_data:

            return {
                "success": False,
                "message": "Expense not found"
            }, 404

        # UPDATE AMOUNT
        if 'amount' in data:

            try:

                amount = float(
                    data['amount']
                )

            except Exception:

                return {
                    "success": False,
                    "message": "Amount must be a number"
                }, 400

            if amount <= 0:

                return {
                    "success": False,
                    "message": "Amount must be positive"
                }, 400

            expense_data.amount = amount

        # UPDATE CATEGORY
        if 'category' in data:

            if data['category'] not in ALLOWED_CATEGORIES:

                return {
                    "success": False,
                    "message": f"Category must be one of {ALLOWED_CATEGORIES}"
                }, 400

            expense_data.category = data['category']

        # UPDATE DESCRIPTION
        if 'description' in data:

            expense_data.description = data['description']

        db.session.commit()

        return {
            "success": True,
            "message": "Expense updated successfully",
            "expense": {
                "id": expense_data.id,
                "amount": expense_data.amount,
                "category": expense_data.category,
                "description": expense_data.description,
                "user_id": expense_data.user_id,
                "created_at": str(
                    expense_data.created_at
                ) if expense_data.created_at else None
            }
        }, 200

    except Exception as e:

        traceback.print_exc()

        db.session.rollback()

        return {
            "success": False,
            "error": str(e)
        }, 500