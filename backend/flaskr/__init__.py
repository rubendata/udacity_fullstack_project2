import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    migrate = Migrate(app, db)

    # check if this is still needed: /api/*
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response


# ENDPOINTS

    @app.route("/categories")
    def get_categories():
        categories = Category.query.all()
        types = []
        for category in categories:
            types.append(category.type)

        return jsonify({
            'success': True,
            'categories': types
        })

    @app.route('/questions')
    def get_questions():
        try:
            # pagination
            page = request.args.get("page", 1, type=int)
            start = (page - 1) * 10
            end = start + QUESTIONS_PER_PAGE

            # categories
            categories = Category.query.all()
            formatted_categories = [category.format()
                                    for category in categories]

            # questions
            questions = Question.query.all()
            formatted_questions = [question.format() for question in questions]

            return jsonify({
                'success': True,
                'questions': formatted_questions[start:end],
                'total_questions': len(questions),
                'categories': formatted_categories,
                'current_category': ""
            })
        except Exception as e:
            print(e)

    @app.route("/questions/<question_id>", methods=['DELETE'])
    def get_specific_question(question_id):

        try:
            question = Question.query.filter_by(id=question_id).one_or_none()
            if question_id is None or question is None:
                abort(404)
            question.delete()
            return jsonify({
                'success': True,
                'quesion_id': question_id

            })
        except Exception as e:
            print(e)
            abort(404)

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        search_term = body.get('searchTerm')

        try:
            if search_term is not None:
                questions = Question.query.filter(
                    Question.question.ilike(
                        '%{}%'.format(search_term))).all()
                formatted_questions = [question.format()
                                       for question in questions]
                return jsonify({
                    'success': True,
                    'questions': formatted_questions
                })

            else:
                if body['question'] is None or body['answer'] is None \
                        or body['difficulty'] is None \
                        or body['category'] is None:
                    abort(400)

                question = Question(
                    question=body['question'],
                    answer=body['answer'],
                    difficulty=body['difficulty'],
                    category=body['category'],
                )
                question.insert()
                return jsonify({
                    'success': True,
                    'question': question.format()
                })
        except Exception as e:
            print(e)
            abort(400)

    @app.route("/categories/<category_id>/questions")
    def get_category_questions(category_id):

        if category_id is None:
            abort(400)
        try:
            questions = Question.query.filter_by(category=category_id).all()
            if len(questions) == 0:
                abort(400)
            formatted_questions = [question.format() for question in questions]

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'current_category': category_id
            })
        except Exception as e:
            print(e)
            abort(400)

    @app.route("/quizzes", methods=['POST'])
    def start_quiz():
        body = request.get_json()
        new_questions = []
        try:
            category_id = body["quiz_category"]["id"]
            category_id = int(category_id)
            category_type = body["quiz_category"]["type"]
            previous_questions = body["previous_questions"]
            if category_type == "click":
                questions = Question.query.all()
                formatted_questions = [question.format()
                                       for question in questions]
            else:
                questions = Question.query.filter_by(
                    category=category_id).all()
                formatted_questions = [question.format()
                                       for question in questions]

            # search if random question was already asked
            for question in formatted_questions:
                if question["id"] not in previous_questions:
                    new_questions.append(question)

            # if no more questions left return a dummy question
            if len(new_questions) == 0:
                dummy_question = {
                    "id": 99,
                    "question": "no more questions left in this category",
                    "catgory": category_id,
                    "answer": "add new questions to this category"
                }
                return jsonify({
                    'success': True,
                    'question': dummy_question
                })
            random_number = random.randint(0, len(new_questions) - 1)
            question = new_questions[random_number]

            return jsonify({
                'success': True,
                'question': question
            })
        except Exception as e:
            print(e)
            abort(422)


# ERRORHANDLERS
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable entry"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500
    return app
