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
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route("/")
  def hello():
    return "hello"

  # @app.route('/<category_name>')
  # def get_specific_category(category_name):
  #   category = Category.query.filter(Category.type.ilike(category_name)).first()
  #   join_questions = db.session.query(Category, Question).join(Question).filter(Category.id==category.id).all()
  #   for category, question in join_questions:
  #     #print(question.question)
  #     formatted_questions = [question.format() for category, question in join_questions]

  #   return jsonify({
  #     'success': True,
  #     'Category': category.type,
  #     'questions': formatted_questions,
  #     })
  
  
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
      #current_category = request.form("current_category")
      

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
    try:
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
 
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


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

    