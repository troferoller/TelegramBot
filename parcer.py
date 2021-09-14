import pymongo
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client['Telegram']
students = db['Stud']

i=0
with open("question.txt") as file:
    for line in file:
        i += 1
        question = line.split(",")
        db.Stud.insert_one({f"question{i}": question[0], "answer1": question[1], "answer2": question[2], "answer3": question[3], "answer4": question[4]})


