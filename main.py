import json 
import os 

class Registration():

    @staticmethod
    def sign_up(name,email,pas):       # Duplicate Signup Prevention Logic needed.
        
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
    def __init__(self,file):
        self.file_path = file
        self.total = 0
        self.correct = 0
        self.incorrect = 0
        self.name = ""
        self.points = 0

    def execute(self):
        with open(self.file_path,'r') as f:
            data = json.load(f)

        answers = []
        for q in data['questions']:
            answers.append(q['answer'])

        self.name = data['title']

        idx = 0
        for q in data['questions']:
            print(f"\n{q['question']}")

            num = 1
            for option in q['options']:
                print(f"{num}: {option}")
                num+=1

            user = int(input("Enter Your answer: "))
            if user - 1 == answers[idx]:
                self.correct+=1
                print("Correct")
            else:
                self.incorrect+=1
                print("Incorrect")
            self.total+=1
            idx+=1

        self.points+= self.correct * 2

    def get_stats(self):
        p = (self.correct / self.total) * 100
        d = {
            'name':self.name,
            'total':self.total,
            'correct':self.correct,
            'incorrect':self.incorrect,
            'points':self.points,
            'percentage':p
        }
        return d


class User():
    def __init__(self,name,email,pas):
        self.name = name
        self.email = email
        self.pas = pas
        self.stats = None

    def get_score(self):
        return self.score

    def share_quiz(self):
        all_quizes = os.listdir('Quizes')

        paths = []
        idx = 1
        for quiz in all_quizes:
            
            path = f"Quizes/{quiz}"
            with open(path,'r') as f:
                data = json.load(f)
            
            if self.email in data['authors']:
                print(f"{idx}: {data['title']}")
                paths.append(path)
                idx+=1

        user = int(input("Enter which file you want to share: "))
        code = input("Create a code to share this file: ")
        
        
        file = paths[user-1]

        with open('shared_files.json','r') as f:
            data = json.load(f)

        if file in data:
            print(f"File is already shared and have a code: {data[file]}")
            return False

        data[file] = code

        with open('shared_files.json','w') as f:
            json.dump(data,f,indent=4)

    def load_quiz(self):
        u_code = input("Enter the code of which quiz you wanna load: ")

        with open('shared_files.json') as f:
            data = json.load(f)

        for file,code in data.items():
            if code == u_code:

                with open(file,'r') as f:
                    content = json.load(f)

                content['authors'].append(self.email)


                with open(file,'w') as f:
                    json.dump(content,f,indent=4)

                return True
        return False

    def add_quiz(self,jason):
        data = json.loads(jason)
        data['authors'] = [self.email]
        path = f"Quizes/{data['title'].lower().strip()}.json"

        with open(path,'w') as f:
            json.dump(data,f,indent=4)

    def attempt_quiz(self):
        files = os.listdir('Quizes')
        idx = 1
        l = []
        for file in files:
            with open(f"Quizes/{file}",'r') as f:
                data = json.load(f)
            if self.email in data['authors']:
                print(f"{idx}: {file}")   # The logic for checking that which quiz to be given to user 
                l.append(f"Quizes/{file}")
                idx+=1

        if len(l) == 0:
            return "You dont have any Quiz, Please create one"
        
        user = int(input("Enter which quiz to takle: "))
        q = Quiz(l[user-1])
        q.execute()
        self.stats = q.get_stats()

        with open('all_users_stats.json','r') as f:
            data = json.load(f)

        if self.email in data:
            data[self.email]['total_score']+=self.stats['points']
            data[self.email]['quizzes_taken']+=1
            data[self.email]['history'].append({'quiz':self.stats['name'], 'percentage':self.stats['percentage']})
        else:
            data[self.email] = {
                'name':self.name,
                'total_score':self.stats['points'],
                'quizzes_taken':1,
                'history':[{'quiz':self.stats['name'], 'percentage':self.stats['percentage']}]
            }

        with open('all_users_stats.json','w') as f:
            json.dump(data,f,indent=4)


class Leaderboard():

    @staticmethod
    def rank_total_score():
        with open('all_users_stats.json','r') as f:
            data = json.load(f)

        d = {}
        for user in data:
            d[user] = data[user]['total_score']

        sorted_d = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
        return sorted_d

    @staticmethod
    def rank_quizes_taken():
        with open('all_users_stats.json','r') as f:
            data = json.load(f)

        d = {}
        for user in data:
            d[user] = data[user]['quizzes_taken']

        sorted_d = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
        return sorted_d 

    @staticmethod
    def rank_performance():
        with open('all_users_stats.json','r') as f:
            data = json.load(f)

        d = {}

        for user in data:
            d[user] = [0,0]
            for p in data[user]['history']:
                d[user][0]+=1
                d[user][1]+=p['percentage']

        final_data = {}

        for user in d:
            avg = d[user][1] / d[user][0]
            final_data[user] = avg

        sorted_final = dict(sorted(final_data.items(), key=lambda item: item[1], reverse=True))
        return sorted_final


class App():
    def __init__(self):
        self.current_user = None
        self.is_running = True

    def show_menu(self):
        if self.current_user is None:
            print("-------- Welcome To Quiz App ----------")
            print("1: Signup")
            print("2: Login")
            print("3: Exit")
        else:
            print(f"--------- Hello {self.current_user.name} ---------")
            print("1: Add Quiz")
            print("2: Attempt Quiz")
            print("3: Share Quiz")
            print("4: Load Quiz from code")
            print("5: See Leaderboard")
            print("6: Logout")

    def run(self):
        while self.is_running:
            self.show_menu()
            choice = int(input("Enter your choice: "))
            self.handle_choice(choice)

    def handle_choice(self,choice):
        if self.current_user is None:
            if choice == 1:
                self.handle_signup()
            elif choice == 2:
                self.handle_login()
            elif choice == 3:
                self.handle_exit()

        else:
            if choice == 1:
                self.handle_add_quiz()
            elif choice == 2:
                self.handle_attempt_quiz()
            elif choice == 3:
                self.handle_share_quiz()
            elif choice == 4:
                self.handle_load_quiz()
            elif choice == 5:
                self.handle_show_leaderboard()
            elif choice == 6:
                self.handle_exit()

    def handle_signup(self):
        name = input("Enter Your name: ")
        email = input("Enter your email: ")
        pas = input("Create a strong password: ")

        result = Registration.sign_up(name,email,pas)

        if result:
            print("Your account has been created successfully.")
        else:
            print("A user with this email already exist")

    def handle_login(self):
        email = input("Enter your email: ")
        pas = input("Enter your password: ")

        result = Registration.login(email,pas)

        if result:
            print("Login Successfull")
            self.current_user = result
        else:
            print("Login Failed")

    def handle_exit(self):
        print("Thanks for using, Goodbye!")
        self.is_running = False

    def handle_add_quiz(self):
        jason = input("Enter your json: ")
        self.current_user.add_quiz(jason)
        print("Quiz added successfully")

    def handle_attempt_quiz(self):
        self.current_user.attempt_quiz()

    def handle_share_quiz(self):
        self.current_user.share_quiz()

    def handle_load_quiz(self):
        result = self.current_user.load_quiz()

        if result:
            print("Quiz loaded successfully")
        else:
            print("Invalid code")

    def handle_show_leaderboard(self):
        print("------ Select the ranking category --------")
        print("1: Rank based on points")
        print("2: Rank based on no of quizzes attempt")
        print("3: Rank based on overall percentage")

        user = int(input("Enter your choice: "))

        if user == 1:
            result = Leaderboard.rank_total_score()
        elif user == 2:
            result = Leaderboard.rank_quizes_taken()
        elif user == 3:
            result = Leaderboard.rank_performance()
        else:
            print("Invalid Input given")

        for user in result:
            print(f"{user} : {result[user]}")

    
    
    
app = App()

app.run()

# # Registration.sign_up('Ahmad','ahmad@gmail.com','1122')
# # l = Registration.login('ahmad@gmail.com','1122')

# # l.share_quiz()


# Registration.sign_up('Mustafa','mustafa@gmail.com',2222)
# l2 = Registration.login('mustafa@gmail.com',2222)

# # r = l2.load_quiz()
# # print(r)

# l2.attempt_quiz()

# # # result = l2.attempt_quiz()
# # # print(result)

# # user = input("Enter jason: ")
# # l2.add_quiz(user)

# # l2.attempt_quiz()

# # result = Leaderboard.rank_total_score()
# # result2 = Leaderboard.rank_quizes_taken()

# # print(result)
# # print(result2)

# # r = Leaderboard.rank_performance()
# # print(r)