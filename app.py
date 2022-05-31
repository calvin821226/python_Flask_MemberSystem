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
    if "nickname" in session:
        return render_template("member.html",nickname = session["nickname"])
    else:
        return redirect("/")


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

@app.route("/signin",methods=["POST"])
def signin():
    #從前端取得使用者輸入
    email = request.form["email"]
    password = request.form["password"]
    #和DB做互動，比對帳密
    collection = db.users
    result = collection.find_one(
        {"$and":[
            {"email":email},
            {"password":password}
        ]}
    )
    print(result)

    if result != None:
        session["nickname"] = result["nickname"]
        return redirect("/member")
    #找不到對應資料，登入失敗，導向到錯誤頁面
    return redirect("/error?msg=帳密錯誤")

@app.route("/signout")
def signout():
    #移除Session中的會員資訊
    del session["nickname"]
    return redirect("/")
  
app.run(port = 8080)

