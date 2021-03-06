import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

       
    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        data_length = len(data["questions"])
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data_length,10)

        res = self.client().get("/questions?page=1000")    
        self.assertEqual(res.status_code,404)
        
        
    def test_create_new_question(self):
        res = self.client().post("/questions", json=(
            {'question':'test question', 
            'answer':'test answer', 
            'category':1, 
            'difficulty':1}
            )
            )
        self.assertEqual(res.status_code,200)
    
    def test_create_new_question_400(self):
        res = self.client().post("/questions", json=(
            {'question':'test question', 
            'answer':'test answer', 
            'difficulty':1}
            )
            )
        self.assertEqual(res.status_code,400)
    
    def test_delete_question(self):
        """Test /questions/<question_id>  DELETE"""
        questions = Question.query.all()
        last_question = questions[len(questions)-1]
        res = self.client().delete("/questions/{}".format(last_question.id))
        self.assertEqual(res.status_code,200)
        empty = ""
        res = self.client().delete("/questions/{}".format(empty))
        self.assertEqual(res.status_code,404)

    def test_get_categories(self):
        res = self.client().get("/categories")
        self.assertEqual(res.status_code,200)
        res = self.client().get("/categories/99")
        self.assertEqual(res.status_code,404)
        
    def test_search_question(self):
        res = self.client().post("/questions", json=({'searchTerm':"test"}))
        self.assertEqual(res.status_code,200)
        res = self.client().post("/questions", json=({'searchTerm':""}))
        self.assertEqual(res.status_code,200)
        res = self.client().post("/questions", json=({'searchTerm':"vbsjrjhgsejhvgsehkgvkgvsehgcsehgbf"}))
        self.assertEqual(res.status_code,200)
        res = self.client().post("/questions", json=({'searchTerm':None}))
        self.assertEqual(res.status_code,400)
        
        
    def test_get_category_questions(self):
        res = self.client().get("/categories/1/questions")
        self.assertEqual(res.status_code,200)
    
        res = self.client().get("/categories/2/questions")
        self.assertEqual(res.status_code,200)

        res = self.client().get("/categories/99/questions")
        self.assertEqual(res.status_code,400)

    def test_quizzes(self):
        res = self.client().post("/quizzes", json=(
            {"quiz_category": {"id": 0, "type": "Science"}, 
            "previous_questions": [20,21,22]
            }))
        self.assertEqual(res.status_code,200)
        res = self.client().post("/quizzes", json=(
            {"quiz_category": None, 
            "previous_questions": [20,21,22]
            }))
        self.assertEqual(res.status_code,422)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()