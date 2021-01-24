import random

previous_questions = []
questions = [{"id":1, "type":2}, {"id":2, "type":2},{"id":3, "type":0}]


# while len(questions)>0:
#     random_id = random.randint(0,len(questions)-1)
#     print("random_id: {}".format(random_id))
#     question = questions[random_id]
#     print("question: {}".format(question))
#     del questions[random_id]
#     print("questions: {}".format(questions))
#     previous_questions.append(question["id"])
#     print("previous_questisons: {}".format(previous_questions))

print("vorher: {}".format(questions))
previous_questions = [1, 2,3]
new_questions = []
for question in questions:
    if question["id"] not in previous_questions:
        new_questions.append(question)
print("new_questions: {}".format(new_questions))