import logInApplication
import connection

def main():
    print("PyMessager")
    userId = logInApplication.logInToAccount()

    print("\n\nWelcome to PyMessager\n")
    startApplication(userId)
    appFeatures(userId)

def startApplication(userId):
    idUsers = connection.DatabaseQueries.getIdFromCorrespondences(userId)

    if not idUsers:
        print("--> no messages <--")
    else:
        correspondences(idUsers, userId)

def correspondences(idUsers, userId):
    loginsData = connection.DatabaseQueries.idsToLogins(idUsers)
    print("Correspondences -->\n")
    for key, value in loginsData.items():
        mess = ""
        if not connection.DatabaseQueries.getStatus(userId, key):
            mess = "(new message)"
        print("user -> ", value, mess)

def appFeatures(userId):
    print("\nFunctions --> \n1.Creating correspondence 2.Open correspondence 3.Log out of your account 4.Delete account")
    choise = input("Your choise - ")

    if choise == '1':
        print("CREATE CORRESPONDENCE")
        createCorrespondence(userId)
    elif choise == '2':
        print("OPEN CORRESPONDENCE")
        openCorrespondence(userId)
    elif choise == '3':
        print("LOGOUT FROM ACCOUNT")
        logOut()
    elif choise == '4':
        print("DELETE ACCOUNT")
        deleteAccount(userId)
    else:
        print("you entered something wrong, try again")
        appFeatures(userId)

def createCorrespondence(userId):
    user_login_with = input("enter the login with which you want to create a correspondence - ")
    if not connection.DatabaseQueries.isLoginExist(user_login_with):
        print("such user does not exist, try again")
        createCorrespondence(userId)

    user_id_with = connection.DatabaseQueries.getId(user_login_with)
    if connection.DatabaseQueries.isCorrespondenceExsist(userId, user_id_with):
        print("this correspondence already exists")
        startApplication(userId)
        appFeatures(userId)

    id_correspondence = connection.DatabaseQueries.addCorrespondence_getId(userId, user_id_with)
    messages(userId, id_correspondence, user_id_with)

def messages(userId, id_correspondence, user_id_with):
    print("-E-N-T-E-R--$--I-f--Y-O-U--W-A-N-T--T-O--R-E-T-U-R-N-")
    message = input("your message - ")
    if message == '$':
        startApplication(userId)
        appFeatures(userId)

    connection.DatabaseQueries.correspondencesIsNotRead(id_correspondence, user_id_with)
    connection.DatabaseQueries.setMessage(userId, user_id_with, id_correspondence, message)
    messages(userId, id_correspondence, user_id_with)

def openCorrespondence(userId):
    user_login = input("write to the user - ")
    user_id_with = connection.DatabaseQueries.getId(user_login)

    if not connection.DatabaseQueries.isCorrespondenceExsist(userId, user_id_with):
        print("\n--This correspondence does not exist, create one--\n")
        startApplication(userId)
        appFeatures(userId)

    idCorrespondence = connection.DatabaseQueries.getIdCorrespondence(userId, user_id_with)

    messages_data = connection.DatabaseQueries.getMessages(idCorrespondence, userId)
    for row in messages_data:
        print("-------------------------")
        if row['sender'] != "you":
            print(user_login, " --> ", row['message'], " || ", row['send_time'], "||")
        else:
            status = "repaired"
            if not row['status']:
                status = "unread"

            print("you --> ", row['message'], " || ", row['send_time'], " || [", status, "]")

    connection.DatabaseQueries.messageReadByUser(idCorrespondence, userId)
    connection.DatabaseQueries.correspondenceIsRead(idCorrespondence, userId)

    print()
    messages(userId, idCorrespondence, user_id_with)

def logOut():
    main()

def deleteAccount(userId):
    connection.DatabaseQueries.deleteAccount(userId)
    main()

main()