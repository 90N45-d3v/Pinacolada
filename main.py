from flask import Flask, request, render_template, session, redirect
import time
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(128)


with open("config/server.conf") as f:
    file = f.read()
    host = file.partition("IP: ")[2].partition("\n")[0]
    port = file.partition("Port: ")[2].partition("\n")[0]
    passwd = file.partition("Password: ")[2].partition("\n")[0]

t = time.localtime()
start_day = time.strftime("%d.%m.%Y", t)
start_time = time.strftime("%H:%M", t)

@app.route("/")
def index():
    if session.get("passwd") and session["passwd"] == passwd:

        return render_template("index.html", start_day=start_day, start_time=start_time)
    else:
        return redirect("/login", code=302)

@app.route("/copyright")
def copyright():
    if session.get("passwd") and session["passwd"] == passwd:
        return render_template("copyright.html")
    else:
        return redirect("/login", code=302)

@app.route("/settings")
def settings():
    if session.get("passwd") and session["passwd"] == passwd:
        return render_template("settings.html")
    else:
        return redirect("/login", code=302)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_pass = request.form["passwd"]
        if user_pass == passwd:
            session["passwd"] = user_pass
            return redirect("/", code=302)
        else:
            return render_template("login.html", message="Password incorrect!")

    else:
        return render_template("login.html", message="")

if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)