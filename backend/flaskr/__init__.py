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
  migrate = Migrate(app,db)
  
  cors = CORS(app, resources={r"*": {"origins": "*"}}) ##check if this is still needed: /api/*

  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

 
  @app.route("/")
  def hello():
    return "hello"

    
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
      #pagination
      page= request.args.get("page",1,type=int)
      start = (page-1)*10
      end = start + QUESTIONS_PER_PAGE
      
      #categories
      categories = Category.query.all()
      formatted_categories = [category.format() for category in categories]
      

      #questions
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

  @app.route("/questions/<question_id>", methods=['DELETE']) #this will be the delete route
  def get_specific_question(question_id):
    
    try:
      question = Question.query.filter_by(id=question_id).one_or_none()
      if question_id==None or question==None:
        abort(404)
      question.delete()
      return jsonify({
        'success': True,
        'quesion_id': question_id
        
        })
    except Exception as e:
      print(e)
 
  
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    search_term = body.get('searchTerm')
    
    try:
      if search_term is not None:
        questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
        formatted_questions = [question.format() for question in questions]
        return jsonify({
          'success': True,
          'questions': formatted_questions
        })

      else:
        question = Question(
          question = body['question'],
          answer = body['answer'],
          difficulty = body['difficulty'],
          category = body['category'],
          )
        question.insert()
        return jsonify({
          'success': True,
          'question': question.format()
        })
    except Exception as e:
      print(e)
 
  
  @app.route("/categories/<category_id>/questions")
  def get_category_questions(category_id):
      
      #category_id_for_filter = int(category_id)+1
      questions = Question.query.filter_by(category=category_id).all()
      formatted_questions = [question.format() for question in questions]
      
      return jsonify({
        'success': True,
        'questions': formatted_questions,
        'current_category': category_id
        })

 

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    