# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from scuec_auth import SCUECAuth

app  = Flask(__name__)
sa = SCUECAuth()
sa.open_session_cache()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    uname = str(request.form.get('username')).strip()
    passwd = str(request.form.get('password')).strip()
    if SCUECAuth.is_username_valid(uname) and len(passwd)!=0:
        if sa.login(uname, passwd):
            return '1'
    return '0'

if __name__ == '__main__':
    app.run()
