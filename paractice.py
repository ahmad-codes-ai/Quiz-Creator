import json

def name(text):
    return 'musupa@chomu.com'

with open('users.json','w') as f:
    initial_data = {'main_list':[]}
    json.dump(initial_data,f)

class Quiz():

    def __init__(self,jason):
        self.jason = jason
    
    def execute_quiz(self):
        ''' This will take json and make it run like test check how mnay correct answers. '''
        print("Success") 

    def get_name(self):
        return self.jason + 'hh'

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
        quiz = Quiz(jason)
        self.quizes.append(quiz)

    def attempt_quiz(self):
        idx = 0
        for quiz in self.quizes:
            print(f"{idx} : {quiz.get_name()}")
            idx+=1
        user = int(input("Enter the number of quiz you want to takle: "))
        self.quizes[user].execute_quiz()

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

class Leaderboard():
    def __init__(self):
        self.users = []

    def add_user(self,user):
        if user not in self.users:
            self.users.append(user)
            return True
        return False

    


Registration.sign_up('Ahmad','ahmad@gmail.com',12345)
user1 = Registration.login('ahmad@gmail.com',12345)

Registration.sign_up('Mustafa','mustafa@gmail.com',2222)
user2 = Registration.login('mustafa@gmail.com',2222)

current = user2

print(current.get_score())

user1.add_quiz('hello')
user1.add_quiz('burger')
user1.add_quiz('helloagain')
print(user1.quizes)
user1.attempt_quiz()