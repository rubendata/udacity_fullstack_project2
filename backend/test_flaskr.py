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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # def test_get_specific_category(self):
    #     """Test /<category_name> GET"""
    #     categories = Category.query.all()
    #     for category in categories:
    #         res = self.client().get(category.type)
    #         self.assertEqual(res.status_code,200)
    def test_get_root_hello(self):
        """Test /<category_name> GET"""
        res = self.client().get("/")
        self.assertEqual(res.status_code,200)

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        data_length = len(data["questions"])
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data_length,10)
    
    def test_get_specific_question(self):
        """Test /questions/<question_id>  GET"""
        res = self.client().get("questions/5")
        self.assertEqual(res.status_code,200)
        res = self.client().get("questions/1") #id 1 does not exist
        self.assertEqual(res.status_code,404)
        res = self.client().get("questions/") #id empty should be 404
        self.assertEqual(res.status_code,404)
        
    def test_create_new_question(self):
        res = self.client().post("/questions", json=(
            {'question':'test question', 
            'answer':'test answer', 
            'category':1, 
            'difficulty':1}
            )
            )
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code,200)
    
    def test_get_categories(self):
        res = self.client().get("/categories")
        self.assertEqual(res.status_code,200)
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()