import json 
import os 

class Registration():

    @staticmethod
    def sign_up(name,email,pas):

        with open('users.json','r') as f:
            data = json.load(f)

        data['main_list'].append({'name':name,'email':email,'pass':pas})

        with open('users.json','w') as f:
            json.dump(data,f,indent=4)

    @staticmethod
    def login(email,pas):
        with open('users.json','r') as f:
            users = json.load(f)
    
        for user in users['main_list']:
            if user['email'] == email and user['pass'] == pas:
                user = User(user['name'],email,pas)
                return user
        return False

class Quiz():
    def __init__(self,file):
        self.file_path = file

    def execute(self):
        with open(self.file_path,'r') as f:
            data = json.load(f)

        answers = []
        for q in data['questions']:
            answers.append(q['answer'])

        correct = 0
        total = 0
        incorrect = 0
        name = data['title']
        points = 0

        idx = 0
        for q in data['questions']:
            print(f"\n{q['question']}")

            num = 1
            for option in q['options']:
                print(f"{num}: {option}")
                num+=1

            user = int(input("Enter Your answer: "))
            if user - 1 == answers[idx]:
                correct+=1
                print("Correct")
            else:
                incorrect+=1
                print("Incorrect")
            total+=1
            idx+=1

        points+= correct * 2

        d = {
            'name':name,
            'total':total,
            'correct':correct,
            'incorrect': incorrect,
            'points':points
        }

        return d
        
        
        


class User():
    def __init__(self,name,email,pas):
        self.name = name
        self.email = email
        self.pas = pas
        self.score = 0
        self.quizes = []

    def get_score(self):
        return self.score

    def add_quiz(self,jason):
        data = json.loads(jason)
        data['author'] = self.email
        path = f"Quizes/{data['title'].lower().strip()}.json"

        with open(path,'w') as f:
            json.dump(data,f,indent=4)

    def attempt_quiz(self):
        files = os.listdir('Quizes')
        idx = 1
        l = []
        for file in files:
            print(f"{idx}: {file}")
            l.append(f"Quizes/{file}")
            idx+=1
        user = int(input("Enter which quiz to takle: "))
        q = Quiz(l[user-1])
        q.execute()

Registration.sign_up('Ahmad','ahmad@gmail.com','1122')
l = Registration.login('ahmad@gmail.com','1122')


l.attempt_quiz()


