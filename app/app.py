from flask import Flask, request, render_template, session, flash
import db_articles, db_users

app = Flask(__name__)
app.secret_key = 'b52635eab6be8ca4c07bd65adc04b27d11a8e251b1e3d16825b881497b1c7af0'

@app.route("/")
def login():
    if 'username' in session:
        return render_template('home.html')
    return render_template('login.html')

# the home page; if the user is not logged in, redirect to login page
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get("sub0") == "login":
            username = request.form['username']
            password = request.form['password']
            session['username'] = username
            return render_template('home.html')
        if request.form.get("sub1") == "register":
            new_username = request.form['new_username']
            new_password = request.form['new_password']
            if db_users.username_in_system(new_username):
                flash('Username already in use')
                return render_template('login.html')
            else:
                db_users.signup(new_username, new_password)
                session['username'] = new_username
                flash('Account created')
                return render_template('home.html')
        else:
            if "" == username and "" == password:
                return render_template('login.html', error = "Enter a username and password.") # TODO: add error message
            elif "" == username or "" == password:
                return render_template('login.html', error = "Enter a username or password") # TODO: add error message
            # for incorrect username/password
            if db_users.username_in_system(username) != username or db_users.get_password(username) != password:
                return render_template('login.html', error = "Wrong username or password.") # TODO: add error message
    return render_template('login.html')

# the webpage for creating stories
@app.route('/create', methods=['GET', 'POST'])
def create():
    username = session['username']
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title needed.')
        elif not content:
            flash('Content needed.')
        else:
            db_articles.add_entry(title, content, username)
            return render_template('display.html') # TODO: change this to an added story screen or smth
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
            db_articles.add_entry(title, edit, session['username'])

@app.route('/logout')
def logout():
    db_users.remove_user(session['username'])
    session.pop('username', None) # remove the username from the session if it's there
    return render_template('login.html', error = "Successfully logged out.")

if __name__ == "__main__":
    app.debug = True 
    app.run() 