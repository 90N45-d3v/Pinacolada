from flask import Flask, request, render_template, session, redirect
import re
import time
import secrets
import coconut
import multiprocessing

app = Flask(__name__)
app.secret_key = secrets.token_hex(128)

with open("config/server.conf", "r") as f:
    file = f.read()
    host = file.partition("IP: ")[2].partition("\n")[0]
    port = file.partition("\nPort: ")[2].partition("\n")[0]
    passwd = file.partition("Password: ")[2].partition("\n")[0]

    deauth_limit = file.partition("Deauth: ")[2].partition("\n")[0]
    disassoc_limit = file.partition("Disassoc: ")[2].partition("\n")[0]
    auth_limit = file.partition("Auth: ")[2].partition("\n")[0]
    eviltwin_unenc = file.partition("Unencrypted: ")[2].partition("\n")[0]

t = time.localtime()
start_day = time.strftime("%d.%m.%Y", t)
start_time = time.strftime("%H:%M", t)

def flask_start():
    app.run(host=host, port=port)

@app.route("/")
def index():
    if session.get("passwd") and session["passwd"] == passwd:
        with open("config/server.conf", "r") as f:
            file = f.read()
            deauth_count = file.partition("Deauth Count: ")[2].partition("\n")[0]
            disassoc_count = file.partition("Disassoc Count: ")[2].partition("\n")[0]
            auth_count = file.partition("Auth Count: ")[2].partition("\n")[0]
        return render_template("index.html", start_day=start_day, start_time=start_time, deauth_count=deauth_count, disassoc_count=disassoc_count, auth_count=auth_count)
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
    with open("config/server.conf", "r") as f:
        file = f.read()
        host = file.partition("IP: ")[2].partition("\n")[0]
        port = file.partition("\nPort: ")[2].partition("\n")[0]

        deauth_limit = file.partition("Deauth: ")[2].partition("\n")[0]
        disassoc_limit = file.partition("Disassoc: ")[2].partition("\n")[0]
        auth_limit = file.partition("Auth: ")[2].partition("\n")[0]
        eviltwin_unenc = file.partition("Unencrypted: ")[2].partition("\n")[0]

        mail_sender = file.partition("\nMail: ")[2].partition("\n")[0]
        smtp_server = file.partition("SMTP Server: ")[2].partition("\n")[0]
        smtp_port = file.partition("SMTP Port: ")[2].partition("\n")[0]
        mail_reciever = file.partition("\nTo: ")[2].partition("\n")[0]

    if session.get("passwd") and session["passwd"] == passwd:
        if request.method == "POST":
            user_ip = request.form["user_ip"]
            user_port = request.form["user_port"]
            user_pass = request.form["user_pass"]

            user_deauth = request.form["user_deauth"]
            user_disassoc = request.form["user_disassoc"]
            user_auth = request.form["user_auth"]

            user_mail_sender = request.form["user_mail_sender"]
            user_smtp_server = request.form["user_smtp_server"]
            user_smtp_port = request.form["user_smtp_port"]
            user_mail_sender_pass = request.form["user_mail_sender_pass"]
            user_mail_reciever = request.form["user_mail_reciever"]

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
            if user_auth:
                config = re.sub("\nAuth: .*?\n", "\nAuth: " + user_auth + "\n", config, flags=re.DOTALL)
            if "user_unencrypted_eviltwin" in request.form:
                config = re.sub("\nUnencrypted: .*?\n", "\nUnencrypted: true" + "\n", config, flags=re.DOTALL)
            if not "user_unencrypted_eviltwin" in request.form:
                config = re.sub("\nUnencrypted: .*?\n", "\nUnencrypted: flase" + "\n", config, flags=re.DOTALL)
            if user_mail_sender:
                config = re.sub("\nMail: .*?\n", "\nMail: " + user_mail_sender + "\n", config, flags=re.DOTALL)
            if user_smtp_server:
                config = re.sub("\nSMTP Server: .*?\n", "\nSMTP Server: " + user_smtp_server + "\n", config, flags=re.DOTALL)
            if user_smtp_port:
                config = re.sub("\nSMTP Port: .*?\n", "\nSMTP Port: " + user_smtp_port + "\n", config, flags=re.DOTALL)
            if user_mail_sender_pass:
                config = re.sub("\nMail Pass: .*?\n", "\nMail Pass: " + user_mail_sender_pass + "\n", config, flags=re.DOTALL)
            if user_mail_reciever:
                config = re.sub("\nTo: .*?\n", "\nTo: " + user_mail_reciever + "\n", config, flags=re.DOTALL)
 
            with open("config/server.conf", "w") as f:
                f.write(config)

            if "user_unencrypted_eviltwin" in request.form:
                return render_template("settings.html", ip=host, port=port, deauth_limit=deauth_limit, disassoc_limit=disassoc_limit, auth_limit=auth_limit, eviltwin_unenc="checked", mail_sender=mail_sender, smtp_server=smtp_server, smtp_port=smtp_port, mail_reciever=mail_reciever)
            else:
                return render_template("settings.html", ip=host, port=port, deauth_limit=deauth_limit, disassoc_limit=disassoc_limit, auth_limit=auth_limit, eviltwin_unenc="unchecked", mail_sender=mail_sender, smtp_server=smtp_server, smtp_port=smtp_port, mail_reciever=mail_reciever)
        else:
            if eviltwin_unenc == "true":
                return render_template("settings.html", ip=host, port=port, deauth_limit=deauth_limit, disassoc_limit=disassoc_limit, auth_limit=auth_limit, eviltwin_unenc="checked", mail_sender=mail_sender, smtp_server=smtp_server, smtp_port=smtp_port, mail_reciever=mail_reciever)
            else:
                return render_template("settings.html", ip=host, port=port, deauth_limit=deauth_limit, disassoc_limit=disassoc_limit, auth_limit=auth_limit, eviltwin_unenc="unchecked", mail_sender=mail_sender, smtp_server=smtp_server, smtp_port=smtp_port, mail_reciever=mail_reciever)
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
    # Delete this if you want to use a single network adapter (no WiFi Coconut)
    print("\n")
    if coconut.check() == "not found":
        print(" * Connect your WiFi Coconut")
        while coconut.check() == "not found":
            time.sleep(1)
    print(" * Starting WiFi Coconut")
    ####
    coconut.start()

    print(" * Starting Guard")
    guard = multiprocessing.Process(target=coconut.guard)
    guard.start()

    print(" * Starting Flask server")
    print("\n --- Flask Server ---")
    flask = multiprocessing.Process(target=flask_start)
    flask.start()