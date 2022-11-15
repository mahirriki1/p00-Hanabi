from flask import Flask, request, render_template, session, flash, redirect
import db_articles, db_users

# made two accounts for testing:
# hi: hii

app = Flask(__name__)
# generated via terminal command: python3 -c 'import secrets; print(secrets.token_hex())'
app.secret_key = 'b52635eab6be8ca4c07bd65adc04b27d11a8e251b1e3d16825b881497b1c7af1'

@app.route("/")
def login():
    if 'username' in session:
        return render_template('home.html')
    return render_template('login.html')

# the home page; if the user is not logged in, redirect to login page
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # for logging in
        if request.form.get("sub0") == "login":
            username = request.form['username']
            password = request.form['password']
            # this set of if statements is for checking if user is in system; if in system, check if password is correct
            # if password is incorrect, return to login page and say wrong password
            if db_users.username_in_system(username):
                if db_users.get_password(username) == password:
                    session['username'] = username
                    print(session)
                    return render_template('home.html')
                else:
                    return render_template('login.html', error = "Wrong password.")
            else:
                # for blank username/password
                if "" == username or "" == password:
                    return render_template('login.html', error = "Enter a username and/or password.")
                # if the username is not found in the database, returns an error with username not in system
                return render_template('login.html', error = "Username not in system.")
        # for registering
        elif request.form.get("sub0") == "register":
            new_username = request.form['new_username']
            new_password = request.form['new_password']
            # to check if username is already registered
            if db_users.username_in_system(new_username):
                return render_template('login.html', error = "Username in system.")
            # for blank username/password
            elif "" == new_username or "" == new_password:
                return render_template('login.html', error = "To register, enter a username and/or password.")
            # if successful, the code under runs and makes an account to the database
            else:
                db_users.signup(new_username, new_password)
                session['username'] = new_username
                print(session)
                return render_template('home.html')
    return render_template('login.html')

#give route to a random story
@app.route('/random', methods=['GET', 'POST'])
def random():
    id = db_articles.get_random_article()
    return redirect(f'/{id}/', code=302)

@app.route('/myStories', methods=['GET', 'POST'])
def myStories():
    username = session['username']
    story_id = db_users.get_list_of_stories(username, 'story_id')
    story_names = []
    for x in story_id:
        temp1 = db_articles.name_from_id(x)
        story_names.append(temp1)
    length = len(story_names)
    return render_template('projects.html', leng = length, a = story_names, b = story_id)

@app.route('/stories', methods=['GET', 'POST'])
def stories():
    story_names = db_articles.get_list_of_stories('story_name')
    story_id = db_articles.get_list_of_stories('story_id')
    length = len(story_names)
    # composition = []
    # for x in range(0, len(story_names)):
    #     temp1 = 
    return render_template('popular.html', leng = length, a = story_names, b = story_id)
# the webpage for creating stories
@app.route('/create', methods=['GET', 'POST'])
def create():
    username = session['username']
    # if request.method == 'POST':
    #     title = request.form['title']
    #     content = request.form['content']
    #     if not title:
    #         flash('Title needed.')
    #     elif not content:
    #         flash('Content needed.')
    #     else:
    #         db_articles.add_entry(title, content, username)
    #         return render_template('display.html') # TODO: change this to an added story screen or smth
    return render_template('create.html')

# webpage for displaying stories
@app.route('/<int:story_id>/', methods=['GET', 'POST'])
def display(story_id):
    text = db_articles.get_full_story_id(story_id)
    title = db_articles.name_from_id(story_id)
    return render_template( 'display.html', display = text, ARTICLE_TITLE=title)

# webpage for editing stories
@app.route('/<int:story_id>/edit/', methods=['GET', 'POST'])
def edit(title):
    story = db_articles.get_full_story(title)
    # if request.method == 'POST':
    #     title = request.form['title']
    #     edit = request.form['edit']
    #     if not title:
    #         flash('Title needed.')
    #     elif not edit:
    #         flash('Edit needed.')
    #     else:
    #         db_articles.add_entry(title, edit, session['username'])
    return render_template('create.html')

@app.route('/logout')
def logout():
    # db_users.remove_user(session['username'])
    session.pop('username', None) # remove the username from the session if it's there
    return render_template('login.html', error = "Logged out.")

if __name__ == "__main__":
    app.debug = True 
    app.run() 