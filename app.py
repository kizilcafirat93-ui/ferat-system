
from flask import Flask, render_template_string, request, redirect, session
import json, datetime

app = Flask(__name__)
app.secret_key = "ferat_system_secret_key"

with open("users.json","r",encoding="utf-8") as f:
    USERS = json.load(f)

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>FERAT SYSTEM</title>
<style>
body {
    background-color:#0b1a2a;
    color:white;
    font-family:Arial;
    text-align:center;
    padding-top:100px;
}
input, button {
    padding:10px;
    margin:5px;
    border-radius:5px;
    border:none;
}
button {
    background-color:#800020;
    color:white;
}
</style>
</head>
<body>
<h1>FERAT SYSTEM</h1>
<form method="post">
<input name="username" placeholder="Kullanıcı adı"><br>
<input name="password" type="password" placeholder="Şifre"><br>
<button type="submit">Giriş Yap</button>
</form>
<p>{{error}}</p>
</body>
</html>
"""

CHAT_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>FERAT SYSTEM</title>
<style>
body {
    background-color:#0b1a2a;
    color:white;
    font-family:Arial;
    padding:20px;
}
.box {
    background-color:#16263a;
    padding:20px;
    border-radius:10px;
}
input {
    width:80%;
    padding:10px;
}
button {
    padding:10px;
    background-color:#800020;
    color:white;
    border:none;
}
</style>
</head>
<body>
<h2>FERAT SYSTEM</h2>
<div class="box">
<p><b>Hoş geldiniz {{name}}, bugün ne yapıyoruz 🙂</b></p>
<p>Saat: {{time}}</p>
<form method="post">
<input name="msg" placeholder="Mesaj yazın">
<button type="submit">Gönder</button>
</form>
<p>{{response}}</p>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def login():
    error=""
    if request.method=="POST":
        u=request.form["username"]
        p=request.form["password"]
        if u in USERS and USERS[u]["password"]==p:
            session["user"]=u
            return redirect("/chat")
        else:
            error="Hatalı giriş"
    return render_template_string(LOGIN_HTML,error=error)

@app.route("/chat", methods=["GET","POST"])
def chat():
    if "user" not in session:
        return redirect("/")
    name=USERS[session["user"]]["name"]
    response=""
    if request.method=="POST":
        msg=request.form["msg"]
        response=f"FERAT SYSTEM: Mesajınız alındı, {name}."
    time=datetime.datetime.now().strftime("%H:%M:%S")
    return render_template_string(CHAT_HTML,name=name,time=time,response=response)

app.run(host="0.0.0.0", port=5000)
