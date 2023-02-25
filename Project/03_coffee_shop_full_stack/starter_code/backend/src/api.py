import os
from os import environ
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''


# db_drop_and_create_all()

# ROUTES

@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    shortened_drinks = [drink.short() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': shortened_drinks
    }), 200


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_detail(payload):
    drinks = Drink.query.all()
    detailed_drinks = [drink.long() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': detailed_drinks
    })


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    body = request.get_json()

    try:
        new_title = body.get('title', None)
        new_recipe = body.get('recipe', None)
        json_new_recipe = json.dumps(new_recipe)

        drink = Drink(title=new_title, recipe=json_new_recipe)
        drink.insert()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })

    except Exception as e:
        print(e)
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    body = request.get_json()
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if not drink:
        abort(404)

    try:
        drink.title = body.get('title', None)
        updated_recipe = body.get('recipe', None)
        drink.recipe = json.dumps(updated_recipe)
        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })

    except Exception as e:
        print(e)
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if not drink:
        abort(404)

    try:
        drink.delete()
        return jsonify({'success': True, 'delete': drink_id})

    except Exception as e:
        print(e)
        abort(422)


# Error Handlers

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'Bad Request'
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": 'Resource not found'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": 'Method Not Allowed'
    }), 405


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error'
    }), 500
