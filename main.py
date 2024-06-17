from module import *
        
hyphen = '-'*70

print(hyphen, "\nWelcome!", "\n")

while True:
    
    print("[1]Register", "[2]Log in", "[3]Exit", "\n")
    choice = input("Type 1, 2 or 3: ")
    print("")   
    
    try:
        if choice == '1':    
    
            username = str(input("Username: "))
            password = str(input("Password: "))
            name = str(input("Name: ")) 
            age = int(input("Age: "))
            weight = float(input("Weight: "))
            weight_goal = float(input("Weight Goal: "))
    
            new_user = User(username, password, name, age, weight, weight_goal)
            new_user.create_db()
            print("Registered successfully!", "\n")
    
    except:        
        print("\n", "This username already exists", "\n")

    if choice == '2':
        username = str(input("Username: "))
        password = str(input("Password: "))
        account = User.login(username, password)
    
        if account:
            
            print("Logging into your account!", "\n")

            while True:
                print(hyphen)
                print("HOME PAGE", "\n")
                print(f'Welcome {username}', "\n")              
                print(home_page(username), "\n")                
                try:
                    last_workout = Workout.get_last_workout(username)
                except:
                    print("No last workout recorded", "\n")                    
                
                print(hyphen)      
                print("[1]Register a workout", "[2]Edit profile", "[3]Search a workout", "[4]Log out", "\n")                
                c = input("Type 1, 2 or 3: ")
                print("")

                if c == '1':            
                    amount = int(input("How many exercises do you want register? "))
                    print("")
                    day = int(input("Day: "))
                    month = int(input("Month: "))
                    year = int(input("Year: "))
                    print("")
                    weight = float(input("Weight: "))
                    print("")
                    exercises = str(input("Exercise: "))
                    sets = int(input("Sets: "))
                    repetitions = int(input("Repetitions: "))
            
                    workout = Workout(username, day, month, year, weight, exercises, sets, repetitions)
                    workout.create_db()

                    for q in range(amount-1):
                        exercises = str(input("Exercise: "))
                        sets = int(input("Sets: "))
                        repetitions = int(input("Repetitions: "))
            
                        workout = Workout(username, day, month, year, weight, exercises, sets, repetitions)
                        workout.create_db()
                    continue
                
                if c == '2':
                    edit_profile(username)
                    continue

                if c == '3':
                    search(username)
                    continue

                if c == '4':
                    break

                else:
                    print("Invalid option, try again")

        else:
            print("Invalid username or password, try again.")
    
    if choice == '3':
        break

    else:
        pass
