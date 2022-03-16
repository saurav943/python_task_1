from flask import Flask, request, jsonify, make_response, render_template, session, flash, redirect, url_for

import jwt

from functools import wraps

import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Demonstrating'



def token_required(func):

    @wraps(func)

    def decorated(*args, **kwargs):

        token = request.args.get('token')

        if not token:

            return jsonify({'Alert!': 'Token is missing!'}), 403

        try:

            data = jwt.decode(token, app.config['SECRET_KEY'],"HS256")

            return "Hello "+ data['user']

        except:

            return jsonify({'Message': 'Invalid token'}), 403

        return func(*args, **kwargs)

    return decorated



@app.route('/')

def home():

    if not session.get('logged_in'):
        return render_template('login.html')
    else:
            return render_template('login.html')

@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your dashboard ! '


@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password']:

        session['logged_in'] = True

        token = jwt.encode({

            'user': request.form['username'],

            'expiration': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)

        },

            app.config['SECRET_KEY'])

        return redirect({'token': token})

    else:

        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})

    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)