import connection

def logInToAccount():
    choice = input("Select function -> 1.registration 2.authorization\n")
    if choice == '1':
        print("REGISTRATION")
        return registration()
    elif choice == '2':
        print("AUTHORIZATION")
        return authorization()
    else:
        print("should have entered 1 or 2, try again")
        logInToAccount()

def registration():
    while True:
        login = input("Enter your login - ")
        password = input("Enter tour password - ")

        if connection.DatabaseQueries.isLoginExist(login):
            print("this login already exist, try again")
            continue
        break

    connection.DatabaseQueries.setLoginAndPassword(login, password)
    id = connection.DatabaseQueries.getId(login)
    print("registration completed successfully!!!")
    return id   

def authorization():
    while True:
        login = input("Enter your login - ")
        password = input("Enter your password - ")

        if not connection.DatabaseQueries.isLoginAndPasswordTrue(login, password):
            print("Incorrect login or password, try again")
            continue
        break
    
    id = connection.DatabaseQueries.getId(login)
    print("authorization completed successfully!!!")
    return id