import collections
from flask import*
import flask
import pymongo
import certifi
from bson.objectid import ObjectId

#Connect to DB
try:
    client = pymongo.MongoClient("mongodb+srv://root:root@mydatabase.barvdpw.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
    db = client.member_system
except Exception:
    print("DB connet error!")
else:
    print("DB connect success!")
 

#Initialize Flask Server
app = Flask(__name__,
            static_folder="public",
            static_url_path="/")
app.secret_key = "calvin821226"

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/member")
def member():
    return render_template("member.html")
#/error?msg=錯誤訊息
@app.route("/error")
def error():
    message=request.args.get("msg","這是錯誤訊息,請聯繫客服!")
    return render_template("error.html",message = message)

@app.route("/signup",methods=["POST"])
def signup():
    #從前端接收資料
    nickname = request.form["nickname"]
    email = request.form["email"]
    password = request.form["password"]
    #print(nickname,email,password)
    #根據收到的資料,和資料庫互動
    collection = db.users

    #檢查是否有已被註冊的信箱
    result = collection.find_one({
        "email":email
    })
    if result != None: 
        return redirect("/error?msg=信箱已被註冊")
    else: #把資料放進資料庫
        collection.insert_one(
            {"nickname":nickname,
             "email":email,
             "password":password}
        )
        return redirect("/")



  
app.run(port = 8080)

