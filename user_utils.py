import sqlServer

con = sqlServer.connect()
cur = con.cursor() #required to execute sql query

def getAllUsers():
    sql = "select * from users"
    cur.execute(sql)

    json = dict()

    rows = cur.fetchall()
    for r in rows:
        userID = r[0]
        name = r[1]
        email = r[2]
        password = r[3]
        json[userID] = {'name': name, 'email': email, 'password': password}
    return json

def isUserExist(info:str, password:str):
    # info is email or username
    sql = "select * from users where (name = ? or email = ?) and password = ?"
    cur.execute(sql, (info, info, password))
    return bool(cur.fetchone()) 
#fetchone return a tuple consist of datas in 1 row of table from sql
#if tuple is empty, it is considered false. Same thing to list, set, dict, string    

class user:
    userId: int
    username: str
    email: str
    password: str

def getUser(info:str, password:str):
    sql = "select * from users where (name = ? or email = ?) and password = ?"
    cur.execute(sql, (info, info, password))
    result = cur.fetchone()
    if result:
        resultUser = user()
        resultUser.userId = result[0]
        resultUser.username = result[1]
        resultUser.email = result[2]
        resultUser.password = result[3]
        return resultUser
    return None


def insertUser(name, email, password):
    sql = "insert into users (name, email, password) values (?, ?, ?)"
    cur.execute(sql, (name, email, password))
    con.commit()

def insertNotebook(user_id: int, title: str, note_content: str):
    if not (title and note_content) or not user_id:
        return
    sql = "insert into notebook (user_id, title, note_content) values (?, ?, ?)"
    cur.execute(sql, (user_id, title, note_content))
    con.commit()

def updateNotebook(note_id: int, title: str, note_content: str):
    if not (title and note_content) or not note_id:
        return
    sql = "update notebook set title = ?, note_content = ? where note_id = ?"
    cur.execute(sql, (title, note_content, note_id))
    con.commit()

if __name__ == "__main__":
    # i =  isUserExist("John Doe", "hashed_password")
    # print(i) # >>> false
    insertNotebook(1, "notebook1", "content1")
