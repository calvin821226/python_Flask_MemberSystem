from flask import*
import flask
import pymongo
import certifi
from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb+srv://root:root@mydatabase.barvdpw.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
#Connect to DB
try:
    db = client.member_system
    client = pymongo.MongoClient("mongodb+srv://root:root@mydatabase.barvdpw.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())
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
    nickname = request.form["nickname"]
    email = request.form["email"]
    password = request.form["password"]
    print(nickname,email,password)
    return "OK"

app.run(port = 8080)

