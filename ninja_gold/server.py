import random
from flask import Flask, render_template, request, redirect, session  # Import Flask to allow us to create our app
app = Flask(__name__)    # Create a new instance of the Flask class called "app"
app.secret_key = 'secret' # set a secret key for security purposes

@app.route('/')
def index():
    if "gold" not in session:
        session['gold'] = 0
        session['activity'] = ""
        session['hitpoints'] = 50
    if session['gold'] >= 100 and session['hitpoints'] >= 0:
        return redirect('/win')
    if session['gold'] < 100 and session['hitpoints'] <= 0:
        return redirect('/lose')
    return render_template("index.html", activity_log=session['activity'])

@app.route('/destroy_session', methods=['POST'])
def reset():
    session.clear()
    return redirect('/')

@app.route('/process_money', methods=['POST'])
def process_money():
    if request.form['building'] == "farm":
        session['hitpoints'] -= 10
        session['amount'] = random.randint(10,20)
        session['gold'] = session['amount'] + session['gold']
        session['activity'] = f"<p class='wins'>You got {session['amount']} gold </p>" + session['activity']
    elif request.form['building'] == "cave":
        session['hitpoints'] -= 5
        session['amount'] = random.randint(5,10)
        session['gold'] = session['amount'] + session['gold']
        session['activity'] = f"<p class='wins'>You got {session['amount']} gold </p>" + session['activity']
    elif request.form['building'] == "house":
        session['hitpoints'] -= 2
        session['amount'] = random.randint(2,5)
        session['gold'] = session['amount'] + session['gold']
        session['activity'] = f"<p class='wins'>You got {session['amount']} gold </p>" + session['activity']
    else:
        session['hitpoints'] -= 5
        session['amount'] = random.randint(-50,50)
        session['gold'] = session['amount'] + session['gold']
        if session['amount'] >= 0:
            session['activity'] = f"<p class='wins'>You got {session['amount']} gold </p>" + session['activity']
        else:
            session['activity'] = f"<p class='losses'>You got {session['amount']} gold </p>" + session['activity']
    return redirect('/')

@app.route("/win")
def win():
    return render_template('win.html')

@app.route("/lose")
def lose():
    return render_template('lose.html')

@app.route("/more_hp", methods=['POST'])
def more_hp():
    session['hitpoints'] += 20
    return redirect('/')

if __name__ == "__main__":  # Ensure this file is being run directly and not from a different module
    app.run(debug=True)    # Run the app in debug mode.

