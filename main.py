from flask import Flask, request, render_template, session, redirect
import re
import time
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(128)


with open("config/server.conf", "r") as f:
    file = f.read()
    host = file.partition("IP: ")[2].partition("\n")[0]
    port = file.partition("Port: ")[2].partition("\n")[0]
    passwd = file.partition("Password: ")[2].partition("\n")[0]

    deauth_limit = file.partition("Deauth: ")[2].partition("\n")[0]
    disassoc_limit = file.partition("Disassoc: ")[2].partition("\n")[0]
    assoc_limit = file.partition("Assoc: ")[2].partition("\n")[0]
    eviltwin_unenc = file.partition("Unencrypted: ")[2].partition("\n")[0]

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

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if session.get("passwd") and session["passwd"] == passwd:
        if request.method == "POST":
            user_ip = request.form["user_ip"]
            user_port = request.form["user_port"]
            user_pass = request.form["user_pass"]

            user_deauth = request.form["user_deauth"]
            user_disassoc = request.form["user_disassoc"]
            user_assoc = request.form["user_assoc"]

            with open("config/server.conf", "r") as f:
                config = f.read()

            if user_ip:
                config = re.sub("\nIP: .*?\n", "\nIP: " + user_ip + "\n", config, flags=re.DOTALL)
            if user_port:
                config = re.sub("\nPort: .*?\n", "\nPort: " + user_port + "\n", config, flags=re.DOTALL)
            if user_pass:
                config = re.sub("\nPassword: .*?\n", "\nPassword: " + user_pass + "\n", config, flags=re.DOTALL)
            if user_deauth:
                config = re.sub("\nDeauth: .*?\n", "\nDeauth: " + user_deauth + "\n", config, flags=re.DOTALL)
            if user_disassoc:
                config = re.sub("\nDisassoc: .*?\n", "\nDisassoc: " + user_disassoc + "\n", config, flags=re.DOTALL)
            if user_assoc:
                config = re.sub("\nAssoc: .*?\n", "\nAssoc: " + user_assoc + "\n", config, flags=re.DOTALL)
            if "user_unencrypted_eviltwin" in request.form:
                config = re.sub("\nUnencrypted: .*?\n", "\nUnencrypted: true" + "\n", config, flags=re.DOTALL)
            else:
                config = re.sub("\nUnencrypted: .*?\n", "\nUnencrypted: true" + "\n", config, flags=re.DOTALL)
 
            with open("config/server.conf", "w") as f:
                f.write(config)

            if "user_unencrypted_eviltwin" in request.form:
                return render_template("settings.html", ip=host, port=port, deauth_limit=deauth_limit, disassoc_limit=disassoc_limit, assoc_limit=assoc_limit, eviltwin_unenc="checked")
            else:
                return render_template("settings.html", ip=host, port=port, deauth_limit=deauth_limit, disassoc_limit=disassoc_limit, assoc_limit=assoc_limit, eviltwin_unenc="unchecked")
        else:
            if eviltwin_unenc == "true":
                return render_template("settings.html", ip=host, port=port, deauth_limit=deauth_limit, disassoc_limit=disassoc_limit, assoc_limit=assoc_limit, eviltwin_unenc="checked")
            else:
                return render_template("settings.html", ip=host, port=port, deauth_limit=deauth_limit, disassoc_limit=disassoc_limit, assoc_limit=assoc_limit, eviltwin_unenc="unchecked")
    else:
        return redirect("/login", code=302)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_pass = request.form["user_pass"]
        if user_pass == passwd:
            session["passwd"] = user_pass
            return redirect("/", code=302)
        else:
            return render_template("login.html", message="INCORRECT LOGIN!")

    else:
        return render_template("login.html", message="")

if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)