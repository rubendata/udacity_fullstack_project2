# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT

This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

## ENDPOITS

### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

Example Response
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

### GET '/questions'
- Fetches a dictionary of 
    - **categories** (list of dictionaries):  contains a list of dictionaries with "id" as key and the "type" as value
    - **current_category** (str): contains the id of the current category
    - **questions** (list of dictionaries):  contains a list of dictionaries containing with "id" as key and "category" (str), "difficulty" (int), "answer" (str) and "question" (str) as values 
    - **success** (boolean): indicates that request was successful
    - **total_questions** (int): returns total number of questions

- Request Arguments: None

Example Response:
```
{
  "categories": [
    {
      "id": 0, 
      "type": "Science"
    }, 
    ...
  ], 
  "current_category": "", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 0, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 0, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    ...
  ], 
  "success": true, 
  "total_questions": 19
}
```

### DELETE '/questions/<question_id>'
- Deletes a specific question and returns
    - **success** (boolean): indicates that request was successful
    - **question_id** (int): returns which question id was deleted

- Request Arguments: question_id (int)

Example Response:
```
{
  "quesion_id": "27", 
  "success": true
}

```

### POST '/questions'
- Creates a new question or searches for question

#### Create a new question:
- Takes arguments for 
    - answer (str)
    - category (int)
    - difficulty (int)
    - question (str)
- Returns
    - **question** (dict): shows the answer, category, diffulty and question provided by the request and the id the question got in the database
    - **success** (boolean): indicates that request was successful

    

- Request Arguments: answer, category, difficulty, question

Example Response:
```
{
  "question": {
    "answer": "answer test", 
    "category": 2, 
    "difficulty": 1, 
    "id": 27, 
    "question": "question test"
  }, 
  "success": true
}
```
#### Search a question:
- Searches questions with a provided string
- Returns a list of questions
    - **questions** (list): list containing the question dictionaries that match the search term
    - **success** (boolean): indicates that request was successful
 
- Request Arguments: searchTerm (str)

Example Response:
```
{
  "question": {
    "answer": "answer test", 
    "category": 2, 
    "difficulty": 1, 
    "id": 27, 
    "question": "question test"
  }, 
  "success": true
}

```

### GET '/categories/<category_id>/questions'
- shows the questions for a specific category
- Returns
    - **questions** (list): a list of question dictionaries for the selected category
    - **success** (boolean): indicates that request was successful
    - **current_category** (str): the id of the selected category


- Request Arguments: question_id (int)

Example Response:
```
{
  "current_category": "0", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 0, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    ...
    
  ], 
  "success": true
}

```

### POST '/quizzes'
- starts the quiz for a given category
- Returns
    - **question** (dict): dictionary of question
    - **success** (boolean): indicates that request was successful
    
- Request Arguments: 
    - **quiz_category** (dict): contains "type" and "id", for example: "quiz_category": {"type":"Geography","id": "2"}}
    - **previous_questions** (list): list of question id's for questions that were already asked

Example Curl: 
```
curl -d '{"previous_questions": [2],"quiz_category": {"type":"Geography","id": "2"}}' -H 'Content-Type: application/json' -X POST http://127.0.0.1:5000/quizzes 
```

Example Response:
```
{
  "question": {
    "answer": "Lake Victoria", 
    "category": 2, 
    "difficulty": 2, 
    "id": 13, 
    "question": "What is the largest lake in Africa?"
  }, 
  "success": true
}

```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```