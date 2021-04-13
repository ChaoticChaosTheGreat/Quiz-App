# from replit import db
from replit.database import Database
import os,random,time
from dotenv import load_dotenv
load_dotenv()
db = Database("")
# replit.db__url = my_secret
def livequiz(username):
  x=''
  while x != 'quit':
    choice = input('''Do you wanna  
    1. create a live quiz 
    or 
    2. join one...''')
    if choice == '1':
      x = 'quit'
      num = ['1','2','3','4','5','6','7','8','9','0']
      letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
      code = random.choice(num)+random.choice(letters)+random.choice(num)+random.choice(letters)+random.choice(num)+random.choice(letters)
      print("Ok now we have to create the questions...")
      try:
        amount=int(input("How many questions?\n"))
      except:
        print("Lets try again shall we?")
        continue
      db[code+'_amount'] = int(amount)
      for i in range(1,(amount+1)):
        question = input(f"What is question {i}: \n")
        while True:
          option1 = input("What is option1?\n")
          option2 = input("What is option2?\n")
          option3 = input("What is option3?\n")
          option4 = input("What is option4?\n")
          answer = input(f'And the correct option is : \n')
          if answer not in ['1','2','3','4']:
            print("Try again")
            print("Try just adding the number of the option")
            continue
          else:
            break
        db[f'{code}_question{i}'] = question
        db[f'{code}_question{i}_option1'] = option1
        db[f'{code}_question{i}_option2'] = option2
        db[f'{code}_question{i}_option3'] = option3
        db[f'{code}_question{i}_option4'] = option4
        db[f'{code}_question{i}_answer'] = answer
      timelimit = input("What is the time limit for the live quiz: ")
      db[f'{code}_time'] = timelimit
      db[code] = 'open'
      print('Your code is \u001b[7m'+code+'\u001b[0m share with whoever you want to the quiz with...')
      input("Press enter the start the quiz\nOnce you start no one else will be able to join!\n")
      db[code] = 'started'
      print("Starting quiz...")
      for ls in range(1,(db[code+'_amount']+1)):
        db[f'{code}_question{ls}_wait'] = 'False'
      for q in range(1,(db[code+'_amount']+1)):
        input(f'''Question {q} is:
        {db[code+'_question'+str(q)]}
        Option 1: {db[code+'_question'+str(q)+'_option1']}
        Option 2: {db[code+'_question'+str(q)+'_option2']}
        Option 3: {db[code+'_question'+str(q)+'_option3']}
        Option 4: {db[code+'_question'+str(q)+'_option4']}
        Press [ENTER] to continue''')
        keys = db.prefix('livequiz_points_')
        lister={}
        for key in keys:
          val = db[key]
          lister[key] = val
        print("The top players are: ")
        for d in range(4):
          try:
            z = max(lister,key = lister.get)
            g = z.replace("livequiz_points_","")
            print(f'{g}: {lister[z]}')
            del lister[z]
          except:
            break
        input("Press [ENTER] to continue")
        db[f'{code}_question{q}_wait'] = 'True'
        os.system("clear")
      for i in range(1,(db[code+'_amount']+1)):
        del db[f'{code}_question{i}']
        del db[f'{code}_question{i}_option1']
        del db[f'{code}_question{i}_option2']
        del db[f'{code}_question{i}_option3']
        del db[f'{code}_question{i}_option4']
        del db[f'{code}_question{i}_answer']
        del db[f'{code}_question{i}_wait']
      del db[code+'_amount']
      del db[f'{code}_time']
      del db[code]
    elif choice == '2':
      x = 'quit'
      while True:
        code = input("What is the code to join with\n")
        if code in db.keys():
          print("Yay!")
          break
        else:
          continue
      if db[code] == 'open':
        print("Joining the game...")
        print("Waiting for the host to start the game...")
        while True:
          if db[code] == 'started':
            break
          else:
            continue
        print("The game has started...")
        points = 0
        for i in range(1,(int(db[code+'_amount']+1))):
          start = time.time()
          answer = input('Type in a option: \n')
          end = time.time()
          okay = end - start
          round(okay)
          if answer == db[f'{code}_question{i}_answer']:
            print("Correct!")
            if okay <= 3:
              points+=1000
            elif okay <= 5:
              points +=900
            elif okay <= 7:
              points+=800
            elif okay <= 9:
              points+=700
            elif okay <= 11:
              points+=600
            else:
              points+=500
          else:
            print("Wrong!")
          db[f'livequiz_points_{username}'] = points
          print(f"Waiting for the host to move on")
          while True:
            if db[f'{code}_question{i}_wait'] == 'True':
                break
            else:
                continue
        print(f"Your total points are {points}")
        time.sleep(1)
        del db[f'livequiz_points_{username}']
      else:
        print("The host has already started the game...")
    else:
      continue

def search(username):
  num_correct=0
  num_wrong = 0
  x = ''
  while True:
    search_query = input("Which quiz do you wanna take: \n")
    if (f'quiz_{search_query}_question1') in db.prefix(""):
      print("Well, I guess we found your quiz...")
      input("Press enter to conitnue...")
      print(f"This quiz was created by "+db[f'quiz_{search_query}_creator'])
      for i in range(1,(int(db["quiz_"+search_query]+1))):
        question = input(db[f'quiz_{search_query}_question{i}']+': ')
        if question == db[f'quiz_{search_query}_question{i}_answer']:
          print('Correct!')
          num_correct+=1
        else:
          print('Wrong!')
          print('The correct answer was: \n '+ db[f'quiz_{search_query}_question{i}_answer'])
          num_wrong+=1
        s = db["quiz_"+search_query+'_question'+str(i)]
        x+=f'\n'+s+': '+question
      break
    else:
      continue
  print(f"Well here's how you did... \n You got {num_correct}/{num_correct+num_wrong}")
  num = db[f'quiz_views_{search_query}']
  num+=1
  db[f'quiz_views_{search_query}'] = num
  if db[f'quiz_response_{search_query}'] == 'True':
    db[f'quiz_myresponse_{search_query}_{username}'] = f'''
    Username: {username}
    {x}
    Score: {num_correct}/{num_correct+num_wrong}'''
  print("Thanks for taking this quiz.")
def delete_txt_file(words):
  f = open('users.txt','r')
  a = words
  lst = []
  for line in f:
    for word in a:
        if word in line:
            line = line.replace(word,'')
    lst.append(line)
  f.close()
  f = open('users.txt','w')
  for line in lst:
    f.write(line)
  f.close()

def user(username):
  print("Type help for a list of commands")
  print('''Commands:
      1. Take a quiz
      2. Create a quiz
      3. Take or create a live quiz
      4. Delete your own account''')
  print('Type in the number of the command to use it...')
  command="none"
  while command != "logout":
    command=input(">>> ").lower()
    if command == "4":
      for quiz in db[f'username_{username}_myquizes']:
        bg = db.prefix[f'quiz_myresponse_{quiz}']
        if db[f'quiz_response_{quiz}'] == "True":
          for bges in bg:
            del db[bges]
        for i in range(1,(int(db[quiz]+1))):
          del db[f'quiz_{quiz}_question{i}']
          del db[f'quiz_{quiz}_question{i}_answer']
          del db[f'quiz_views_{quiz}']
          del db["quiz_"+quiz]
          del db[f'quiz_{quiz}_creator']
          del db[f'quiz_response_{quiz}']
      delete(username)
      quit("Your account was deleted")
    elif command == "help":
      print('''Commands:
      1. Take a quiz
      2. Create a quiz
      3. Take or create a live quiz
      4. Delete your own account''')
    elif command == '1':
      search(username)
    elif command == '3':
      livequiz(username)
    elif command == "2":
      x=True
      while x != False:
        name=input("What is the name of your quiz: \n")
        if name not in db.prefix("quiz_"):
          x = False
        else:
          print("Hmmmm... let's pick a different name...")
      while True:
        try: 
          question_number = int(input("How many questions are in your quiz?"))
        except:
          print("Only number please!")
          continue
      while True:
        r = input("Do you want to record responses for this quiz Yes/No?").lower()
        if r == 'yes':
          db[f'quiz_response_{name}'] = 'True'
          break
        elif r == 'no':
          db[f'quiz_response_{name}'] = 'False'
          break
        else:
          continue
      for i in range(1,(question_number+1)):
        question = input(f"What is question {i}: \n")
        answer = input(f'And the answer: \n')
        db[f'quiz_{name}_question{i}'] = question
        db[f'quiz_{name}_question{i}_answer'] = answer
      db[f'quiz_views_{name}'] = 0
      db[f'quiz_{name}_creator'] = username
      db["quiz_"+name] = question_number
      db[f'username_{username}_myquizes'].append(name)
      print(f"Your quiz has been published in the name of {name}")
    
def moderator(username):
  print("Type help for a list of commands")
  print('''Commands:
      1. Delete a user or yourself
      2. Create a quiz
      3. Delete a quiz that you own
      4. View all repsonses for a quiz
      5. Take a quiz...
      6. Take or create a live quiz''')
  print("TYpe in the number of the command to use it...")
  command="none"
  with open ('users.txt','r') as reader:
     x=reader.read()
  while command != "logout":
    command=input(">>> ").lower()
    if command == "1":
      print(x)
      print('''This list of all people is inaccurate and some users might not exist or be on this list''')
      selfer=input('''Do you want to delete your self y/n or yes/no:\n''').lower()
      if selfer in ['yes','y']:
        
        for quiz in db[f'username_{username}_myquizes']:
          bg = db.prefix[f'quiz_myresponse_{quiz}']
        if db[f'quiz_response_{quiz}'] == "True":
          for bges in bg:
            del db[bges]
        for i in range(1,(int(db[quiz]+1))):
          del db[f'quiz_{quiz}_question{i}']
          del db[f'quiz_{quiz}_question{i}_answer']
          del db[f'quiz_views_{quiz}']
          del db["quiz_"+quiz]
          del db[f'quiz_{quiz}_creator']
          del db[f'quiz_response_{quiz}']
        delete(username)
        break
      else:
        user_delete=input('''Type in the username of  the person who you want to delete:\n''').lower()
        if  db[f"username_{user_delete}_position"] not in ['admin','moderator']:
          for quiz in db[f'username_{user_delete}_myquizes']:
            bg = db.prefix[f'quiz_myresponse_{quiz}']
          if db[f'quiz_response_{quiz}'] == "True":
            for bges in bg:
              del db[bges]
          for i in range(1,(int(db[quiz]+1))):
            del db[f'quiz_{quiz}_question{i}']
            del db[f'quiz_{quiz}_question{i}_answer']
            del db[f'quiz_views_{quiz}']
            del db["quiz_"+quiz]
            del db[f'quiz_{quiz}_creator']
            del db[f'quiz_response_{quiz}']
          delete(username)
        else:
          print('You can\'t delete a admin or moderator')
    elif command == "help":
      print('''Commands:
      1. Delete a user or yourself
      2. Create a quiz
      3. Delete a quiz that you own
      4. View all repsonses for a quiz
      5. Take a quiz...
      6. Take or create a live quiz''')
    elif command == '2':
      x=True
      while x != False:
        name=input("What is the name of your quiz: \n")
        if name not in db.keys():
          x = False
        else:
          print("Hmmmm... let's pick a different name...")
      while True:
        try: 
          question_number = int(input("How many questions are in your quiz?"))
        except:
          print("Only number please!")
          continue
      while True:
        r = input("Do you want to record responses for this quiz Yes/No?").lower()
        if r == 'yes':
          db[f'quiz_response_{name}'] = 'True'
          break
        elif r == 'no':
          db[f'quiz_response_{name}'] = 'False'
          break
        else:
          continue
      for i in range(1,(question_number+1)):
        question = input(f"What is question {i}: \n")
        answer = input(f'And the answer: \n')
        db[f'quiz_{name}_question{i}'] = question
        db[f'quiz_{name}_question{i}_answer'] = answer
      db[f'quiz_views_{name}'] = 0
      db[f'quiz_{name}_creator'] = username
      db["quiz_"+name] = question_number
      db[f'username_{username}_myquizes'].append(name)
      print(f"Your quiz has been published in the name of {name}")
    elif command == '3':
      quiz_name = input("What is the name of the quiz that you want view responses for?\n")
      if db[f'quiz_{quiz_name}_creator'] == username:
        if db['quiz_response_'+quiz_name] == 'True':
          print("All Responses")
          b = db.prefix(f'quiz_myresponse_{quiz_name}')
          for something in b:
            f = db[something]
            print(f)
            print("________________________")
      else:
        print("That's not your quiz!")
    elif command == '4':
      quiz_name = input("What quiz do you want to delete: ")
      if db[f'quiz_{quiz_name}_creator'] == username:
        bg = db.prefix[f'quiz_myresponse_{quiz_name}']
        if db[f'quiz_response_{quiz_name}'] == "True":
          for bges in bg:
            del db[bges]
        for i in range(1,(int(db[quiz_name]+1))):
          del db[f'quiz_{quiz_name}_question{i}']
          del db[f'quiz_{quiz_name}_question{i}_answer']
          del db[f'quiz_views_{quiz_name}']
          del db["quiz_"+quiz_name]
          del db[f'quiz_{quiz_name}_creator']
          del db[f'quiz_response_{quiz_name}']
    elif command == '5':
      search(username)
    elif command == '6':
      livequiz(username)
def admin(username):
  print("Type help for a list of commands")
  command="none"
  while command != "logout":
    command=input(">>> ").lower()
    
    with open ('users.txt','r') as reader:
      x=reader.read()
    if command == "1":
      user_delete=input('''Type in the username of  the person who you want to delete:\n''').lower()
      if  db[f"username_{user_delete}_position"] not in ['admin','moderator']:
        for quiz in db[f'{user_delete}_myquizes']:
          bg = db.prefix[f'quiz_myresponse_{quiz}']
        if db[f'quiz_response_{quiz}'] == "True":
          for bges in bg:
            del db[bges]
        for i in range(1,(int(db[quiz]+1))):
          del db[f'quiz_{quiz}_question{i}']
          del db[f'quiz_{quiz}_question{i}_answer']
          del db[f'quiz_views_{quiz}']
          del db["quiz_"+quiz]
          del db[f'quiz_{quiz}_creator']
          del db[f'quiz_response_{quiz}']
        delete(username)
      else:
        print('You can\'t delete a moderator or admin')
    elif command == "help":
      print('''Commands:
      1. delete
      2. upgrade 
      3. downgrade
      4. Create a quiz
      5. Take a quiz
      6. View responses for a quiz
      7. Delete a quiz
      8. Create or Make a Live quiz
      9. Complete Wipe''')
    elif command == '2':
      print(x)
      print("You can't undo this!")
      person=input("Whose position do you want to upgrade:\n").lower()
      y=input("Do you still want to do this Y/n or Yes/no").lower()
      if y in ["y","yes"]:
        db[f"username_{person}_position"] = "moderator"
      else:
        print("Thanks for thinking this through :)")
    elif command == '3':
      print(x)
      person=input("Whose position do you want to downgrade:\n").lower()
      if db[f"username_{person}_position"] != 'admin':
        db[f'username_{person}_position']="user"
      else:
        print("Don't downgrade a admin!")
    elif command == '4':
      x=True
      while x != False:
        name=input("What is the name of your quiz: \n")
        if name not in db.keys():
          x = False
        else:
          print("Hmmmm... let's pick a different name...")
      try: 
        question_number = int(input("How many questions are in your quiz?"))
      except:
        print("Only number please!")
        continue
      while True:
        r = input("Do you want to record responses for this quiz Yes/No?").lower()
        if r == 'yes':
          db[f'quiz_response_{name}'] = 'True'
          break
        elif r == 'no':
          db[f'quiz_response_{name}'] = 'False'
          break
        else:
          continue
      for i in range(1,(question_number+1)):
        question = input(f"What is question {i}: \n")
        answer = input(f'And the answer: \n')
        db[f'quiz_{name}_question{i}'] = question
        db[f'quiz_{name}_question{i}_answer'] = answer
      db[f'quiz_views_{name}'] = 0
      db[f'quiz_{name}_creator'] = username
      db["username_"+username+"_myquizes"].append(name)
      db["quiz_"+name] = question_number
      print(f"Your quiz has been published in the name of {name}")
    elif command == '5':
      search(username)
    elif command == '6':
      quiz_name = input("What is the name of the quiz that you want view responses for?\n")
      if db['quiz_response_'+quiz_name] == 'True':
        print("All Responses")
        b = db.prefix(f'quiz_myresponse_{quiz_name}')
        for something in b:
          f = db[something]
          print(f)
          print("________________________")
    elif command == '7':
      quiz_name = input("What quiz do you want to delete: ")
      bg = db.prefix(f'quiz_myresponse_{quiz_name}')
      if db[f'quiz_response_{quiz_name}'] == "True":
        for bges in bg:
          del db[bges]
      for i in range(1,(int(db[quiz_name]+1))):
        del db[f'quiz_{quiz_name}_question{i}']
        del db[f'quiz_{quiz_name}_question{i}_answer']
      del db[f'quiz_views_{quiz_name}']
      del db["quiz_"+quiz_name]
      del db[f'quiz_{quiz_name}_creator']
      del db[f'quiz_response_{quiz_name}']
    elif command == '8':
      livequiz(username)
    elif command == '9':
      d = db["username_"+username]
      c = db["username_"+username+'_position']
      g = db["username_"+username+"_myquizes"]
      if input("Are you sure?  Y/N: ").lower() == 'y':
        keys = db.prefix('')
        for key in keys:
          del db[key]
        db[username] = d
        db[username+'_position'] = c
        db[f'{username}_myquizes'] = g
      else:
        print("Good Job that you thought this through.")
def login(username):
  password=input("Password: ")
  os.system('clear')
  if password == db["username_"+username]:
      print(f'Welcome {username}' )
      if  db[f"username_{username}_position"] == 'moderator': 
        moderator(username)
      elif db[f"username_{username}_position"] == 'admin':
        admin(username)
      else: 
        print("hi")
        user(username)
  else:
    print("Wrong password/username!")
  
  return username
def create():
  username=input("What is your username: ").lower()
  password=input("What is your password: ")
  if username not in db.keys():
     with open('users.txt','a') as filer:
       filer.write(f'{username}\n')
     db["username_"+username]=password
     db[f"username_{username}_position"]='user'
     db[f'username_{username}_myquizes'] = []
     print(f"Hi there {username}")
     login(username)
  else:
    print("Sorry someone has took that username")
    create()
def delete(username):
  delete_txt_file(username)
  del db["username_"+username]
  del db[f'username_{username}_position']
  del db[f"username_{username}_myquizes"]
  print("Succesfully deleted your account")
keys = db.prefix("quiz_views_")
lister={}
for key in keys:
  val = db[key]
  lister[key] = val
print("The trending quizes are:")
for i in range(9):
  try:
    z = max(lister,key = lister.get)
    g = z.replace('quiz_views_','')
    z.replace("quiz_views_","")
    print(f'{g}: {lister[z]}')
    del lister[z]
  except:
    break
choice=input("Do you want to login or create a account: ").lower()
if choice in ["1","login"]:
  username=input("Username: ").lower()
  login(username)
elif choice in ["2","create"]:
  create()
