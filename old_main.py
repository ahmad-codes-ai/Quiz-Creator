import json



class Registration():

    @staticmethod
    def sign_up(name,email,pas):

        with open('users.json','r') as f:
            data = json.load(f)

        for user in data['main_list']:
            if user['email'] == email:
                return False
            
        data['main_list'].append({'name':name,'email':email,'pass':pas})

        with open('users.json','w') as f:
            json.dump(data,f,indent=4)
            return True
            

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

    def __init__(self,jason,name=None):
        self.name = name
        self.jason = json.loads(jason)
        self.points = 0
        self.percentage = 0.0

        self.correct_options = []
        for q in self.jason:
            self.correct_options.append(q['answer'])
    
    def execute_quiz(self):
        idx = 0
        correct_answered = 0
        for q in self.jason:
            print(q['question'])
            num = 1
            for op in q['options']:
                print(f"{num} : {op} \n")
                num+=1
      
            user = int(input("Enter the correct option: "))
      
            if user - 1 == self.correct_options[idx]:
                print("Correct \n \n")
                self.points+=2
                correct_answered+=1
            else:
                print("Incorrect \n \n")
            idx+=1
        self.percentage = correct_answered / len(self.jason)

    def get_name(self):
        return self.name

    



class User():
    def __init__(self,name,email,pas):
        self.name = name
        self.email = email
        self.pas = pas
        self.score = 0
        self.history = []
        self.quizes = []

        with open('quizes.json','w') as f:
            data = json.load(f)
        d = {'email':self.email,'quizes':[]}
        data['main_list'].append(d)

    def get_score(self):
        return self.score

    def add_quiz(self,jason):

        quiz = Quiz(jason)
        with open('quizes.json','r') as f:
            data = json.load(f)

        for user in data['main_list']:
            if user['email'] == self.email:
                user['quizes'].append(quiz)

    def load_quizes(self):
        with open('quizes.json','r') as f:
            data = json.load(f)

        for quiz in data['main_list']:
            pass



    def attempt_quiz(self):
        idx = 0
        for quiz in self.quizes:
            print(f"{idx} : {quiz.get_name()}")
            idx+=1
        user = int(input("Enter the number of quiz you want to takle: "))
        self.quizes[user].execute_quiz()
        self.update_score(self.quizes[user].points)

    def update_score(self,points):
        self.score+=points

    def get_score(self):
        return self.score



def main():

    while True:

        print("1: Signup")
        print("2: Login")
        user = int(input("Enter Your Choice: "))

        if user == 1:
            name = input("Enter Your name: ")
            email = input("Enter Your Email: ")
            pas = input("Create a password: ")
            result = Registration.sign_up(name,email,pas)
            if result:
                print('You have successfully created an account plz login')
            else:
                print("Another Account with same email exist")

        elif user == 2:
            email = input("Enter Your Email: ")
            pas = input("Enter your password: ")      
            result = Registration.login(email,pas)
            if result:
                print("Login Successfull")

                while True:
                    print("1: Add Quiz")
                    print("2: Attempt Quiz")
                    print("3: Show Score")
                    print("4: To quit")
                    user = int(input("Enter Your Choice: "))

                    if user == 1:
                        jason = input("Enter jason")
                        result.add_quiz(jason)
                    elif user == 2:
                        result.attempt_quiz()
                    elif user == 3:
                        result.get_score()
                    elif user == 4:
                        break
                    else:
                        print("Plz enter a valid option")
            else:
                print("Incorrect Info")

        elif user == 0:
            break

        else:
            print("Plz enter a valid number")


main()