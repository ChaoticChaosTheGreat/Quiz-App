from replit import db
import os,random,time
def livequiz():
  x=''
  while x != 'quit':
    choice = input('''Do you wanna  
    1. create a live quiz 
    or 
    2. join one...''')
    if choice == '1':
      x = 'quit'
      num = ['1','2','3','4','5','6','7','8','9','0']
      letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',]
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
      print('Your code is '+code+' share with whoever you want to the quiz with...')
      input("Press enter the start the quiz\nOnce you start no one else will be able to join!\n")
      db[code] = 'started'
      print("Starting quiz...")
      for i in range(1,(db[code+'_amount']+1)):
        input(f'''Question {i} is:
        {db[code+'_question'+str(i)]}
        Option 1: {db[code+'_question'+str(i)+'_option1']}
        Option 2: {db[code+'_question'+str(i)+'_option2']}
        Option 3: {db[code+'_question'+str(i)+'_option3']}
        Option 4: {db[code+'_question'+str(i)+'_option4']}
        Press [ENTER] to continue''')
        os.system("clear")
      for i in range(1,(db[code+'_amount']+1)):
        del db[f'{code}_question{i}']
        del db[f'{code}_question{i}_option1']
        del db[f'{code}_question{i}_option2']
        del db[f'{code}_question{i}_option3']
        del db[f'{code}_question{i}_option4']
        del db[f'{code}_question{i}_answer']
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
            if okay == 1:
              points+=1000
            elif okay == 2:
              points +=900
            elif okay == 3:
              points+=800
            elif okay == 4:
              points+=700
            elif okay == 5:
              points+=600
            else:
              points+=500
          else:
            print("Wrong!")
        print(f"Your total points are {points}")
      else:
        print("The host has already started the game...")
    else:
      continue

def search():
  num_correct=0
  num_wrong = 0
  search_query = input("Which quiz do you wanna take: \n")
  if (f'{search_query}_question1') in db.keys():
    print("Well, I guess we found your quiz...")
    input("Press enter to conitnue...")
    print(f"This quiz was created by "+db[f'{search_query}_creator'])
    for i in range(1,(int(db[search_query]+1))):
      question = input(db[f'{search_query}_question{i}']+': ')
      if question == db[f'{search_query}_question{i}_answer']:
        print('Correct!')
        num_correct+=1
      else:
        print('Wrong!')
        print('The correct answer was: \n '+ db[f'{search_query}_question{i}_answer'])
        num_wrong+=1
    print(f"Well here's how you did... \n You got {num_correct}/{num_correct+num_wrong}")
    num = db[f'views_{search_query}']
    num+=1
    db[f'views_{search_query}'] = num
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
  command="none"
  while command != "logout":
    command=input(">>> ").lower()
    if command == "delete":
      delete()
      quit()
    elif command == "help":
      print('''Commands:
      1. Take a quiz
      2. Take or create a live quiz
      3. Delete your own account''')
    elif command == '1':
      search()
    elif command == '2':
      livequiz()
def moderator(username):
  print("Type help for a list of commands")
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
        delete(username)
        break
      else:
        user_delete=input('''Type in the username of  the person who you want to delete:\n''').lower()
        if  db[f"{user_delete}_position"] not in ['admin','moderator']:
          del db[user_delete]
          del db[f'{username}_position']
          delete_txt_file(username)
          print("Succesfully deleted")
        else:
          print('You can\'t delete a admin or moderator')
    elif command == "help":
      print('''Commands:
      1. Delete a user or yourself
      2. Create a quiz
      3. Delete a quiz that you own
      4. Take or create a live quiz''')
    elif command == '2':
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
      for i in range(1,(question_number+1)):
        question = input(f"What is question {i}: \n")
        answer = input(f'And the answer: \n')
        db[f'{name}_question{i}'] = question
        db[f'{name}_question{i}_answer'] = answer
      db[f'views_{name}'] = 0
      db[f'{name}_creator'] = username
      db[name] = question_number
      print(f"Your quiz has been published in the name of {name}")
    elif command == '3':
      quiz_name = input("What quiz do you want to delete: ")
      if db[f'{quiz_name}_creator'] == username:
        for i in range(1,(int(db[quiz_name]+1))):
          del db[f'{quiz_name}_question{i}']
          del db[f'{quiz_name}_question{i}_answer']
        del db[f'views_{quiz_name}']
        del db[quiz_name]
        del db[f'{quiz_name}_creator']
    elif command == '4':
      livequiz()
def admin(username):
  print("Type help for a list of commands")
  command="none"
  while command != "logout":
    command=input(">>> ").lower()
    
    with open ('users.txt','r') as reader:
      x=reader.read()
    if command == "1":
      print(x)
      print("This list of all people is inaccurate and some users might not exist or be on this list")
      user_delete=input('''Type in the username of  the person who you want to delete:\n''').lower()
      if  db[f"{user_delete}_position"] !='admin':
        del db[user_delete]
        del db[f'{username}_position']
        delete_txt_file(username)
        print("Succesfully deleted")
      else:
        print('You can\'t delete a moderator or admin')
    elif command == "help":
      print('''Commands:
      1. delete
      2. upgrade 
      3. downgrade
      4. Create a quiz
      5. Take a quiz
      6. Delete a quiz
      7. Create or Make a Live quiz
      8. Complete Wipe''')
    elif command == '2':
      print(x)
      print("You can't undo this!")
      person=input("Whose position do you want to upgrade:\n").lower()
      y=input("Do you still want to do this Y/n or Yes/no").lower()
      if y in ["y","yes"]:
        db[f"{person}_position"] = "moderator"
      else:
        print("Thanks for thinking this through :)")
    elif command == '3':
      print(x)
      person=input("Whose position do you want to downgrade:\n").lower()
      if db[f"{person}_position"] != 'admin':
        db[f'{person}_position']="user"
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
      for i in range(1,(question_number+1)):
        question = input(f"What is question {i}: \n")
        answer = input(f'And the answer: \n')
        db[f'{name}_question{i}'] = question
        db[f'{name}_question{i}_answer'] = answer
      db[f'views_{name}'] = 0
      db[f'{name}_creator'] = username
      db[name] = question_number
      print(f"Your quiz has been published in the name of {name}")
    elif command == '5':
      search()
    elif command == '6':
      quiz_name = input("What quiz do you want to delete: ")
      for i in range(1,(db[quiz_name]+1)):
        del db[f'{quiz_name}_question{i}']
        del db[f'{quiz_name}_question{i}_answer']
      del db[f'views_{quiz_name}']
      del db[quiz_name]
      del db[f'{quiz_name}_creator']
    elif command == '7':
      livequiz()
    elif command == '8':
      if input("Are you sure? This will wipe you too! Y/N: ").lower() == 'y':
        keys = db.prefix('')
        for key in keys:
          del db[key]
        quit()
      else:
        print("Good Job that you thought this through.")
def login(username):
  password=input("Password: ")
  os.system('clear')
  try:
    if password == db[username]:
      print(f'Welcome {username}' )
      if  db[f"{username}_position"] == 'moderator': 
        moderator(username)
      elif db[f"{username}_position"] == 'admin':
        admin(username)
      else: 
        print("hi")
        user(username)
  except:
    print("Invalid username")
  return username
def create():
  username=input("What is your username: ").lower()
  password=input("What is your password: ")
  if username not in db.keys():
     
     with open('users.txt','a') as filer:
       filer.write(f'{username}\n')
     db[username]=password
     db[f"{username}_position"]='user'
     print(f"Hi there {username}")
     login(username)
  else:
    print("Sorry someone has took that username")
    create()
def delete(username):
  
  password=input("What is your password: ")
  if password == db[username]:
    delete_txt_file(username)
    del db[username]
    del db[f'{username}_position']
    print("Succesfully deleted your account")
keys = db.prefix("views_")
lister={}
for key in keys:
  val = db[key]
  lister[key] = val
sort_orders = sorted(lister.items(), key=lambda x: x[1], reverse=True)
print("The trending quizes are")
for i in sort_orders:
	print(i[0], i[1])
choice=input("Do you want to login or create a account: ").lower()
if choice in ["1","login"]:
  username=input("Username: ").lower()
  login(username)
elif choice in ["2","create"]:
  create()
else:
  print("That answer is invalid")