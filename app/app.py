# TODO: change everything to fit with websites

from flask import Flask, request, render_template, session, flash
import db_articles, db_users

app = Flask(__name__)
app.secret_key = 'b52635eab6be8ca4c07bd65adc04b27d11a8e251b1e3d16825b881497b1c7af0'

username = " "
password = db_users.get_password(username)

@app.route("/")
def login():
    if db_users.username_in_system(username):
        return render_template('home.html')
    return render_template('login.html')

# the home page; if the user is not logged in, redirect to login page
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        usr = request.form['username']
        passw = request.form['password']
        db_users.signup(usr, passw)
    if username in usr and password in passw:
        session['username'] = request.form['username']
        return render_template('home.html')
    # for blank responses
    if "" == usr and "" in passw:
        return render_template('login.html') # TODO: add error message
    elif "" == usr or "" == passw:
        return render_template('login.html') # TODO: add error message
    # for incorrect username/password
    if usr != username or passw != password:
        return render_template('login.html') # TODO: add error message

# the webpage for creating stories
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title needed.')
        elif not content:
            flash('Content needed.')
        else:
            db_articles.add_entry(title, content, username)
            return render_template('display.html')
    return render_template('create.html')

# webpage for displaying stories
@app.route('/<int:story_id>', methods=['GET', 'POST'])
def project():
    return render_template('projects.html')

# webpage for editing stories
@app.route('/<int:story_id>/edit/', methods=['GET', 'POST'])
def edit(title):
    story = db_articles.get_full_story(title)
    if request.method == 'POST':
        title = request.form['title']
        edit = request.form['edit']
        if not title:
            flash('Title needed.')
        elif not edit:
            flash('Edit needed.')
        else:
            db_articles.add_entry(title, edit, username)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return render_template('login.html') # TODO: add a logout message

if __name__ == "__main__":
    app.debug = True 
    app.run() 