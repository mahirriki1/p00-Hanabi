import sqlite3
import random as random
import db_users
db = sqlite3.connect("articles.db", check_same_thread=False)
global c
c = db.cursor()
#Method give you the data given if you already know another data and that data's datatype
#IE: If I want the story_id and I know that the user_id is 20. We can call
#select_from_main(story_id, 20, user_id), which will give us the story_id of that row
#recommend not using user_id
def _select_from(table, data_want, data_give, datatype_give):
    temp = ((c.execute(f'SELECT {data_want} FROM {table} WHERE {datatype_give} ="{data_give}"')).fetchall())
    if(len(temp) > 0):
        return temp[0][0]
    else:
        return 0

def _select_from_main(data_want, data_give, datatype_give):
    temp = ((c.execute(f'SELECT {data_want} FROM main WHERE {datatype_give}="{data_give}"')).fetchall())
    if(len(temp) > 0):
        return temp[0][0]
    else:
        return 0
#get the full story with name
def get_full_story(story_name):
    return _select_from_main('full_story', story_name, 'story_name')
def get_full_story_id(story_id):
    return _select_from_main('full_story', story_id, 'story_id')
def get_newest_edit(story_name):
    return _select_from_main('most_recent', story_name, 'story_name')

def name_from_id(story_id):
    return _select_from_main('story_name', story_id, 'story_id')


#new_entry is a boolean, true if the entry is an edit, false if the entry is a new entry
def add_entry(story_name, newest_edit, user_id, edit):
    pre_story = ""
    story_exist = True
    c.execute("CREATE TABLE if not exists main(story_id INTEGER PRIMARY KEY, story_name TEXT, full_story TEXT, most_recent TEXT, user_id INTEGER, like INTEGER)")
    temp1 = c.execute("SELECT story_id FROM main").fetchall()
    story_id = (_select_from_main('story_id', story_name, 'story_name'))
    prev_add = (_select_from_main('most_recent', story_name, 'story_name'))
    if story_id == 0:
        story_exist = False
        story_id = len(temp1) + 1
        like = 0
    if((not edit) and story_exist):
        return 0
    if(story_exist):
        pre_story = get_full_story(story_name)
        like = _select_from_main('like', story_name, 'story_name')
    new_full = pre_story + " " + newest_edit
    c.execute(f'INSERT OR REPLACE INTO main(story_id, story_name, full_story, most_recent, user_id, like) VALUES (?,?,?,?,?,?)', (story_id, story_name, new_full, newest_edit, user_id, like))
    c.execute(f'CREATE TABLE if not exists "{story_name}"(edit_id INTEGER PRIMARY KEY, newest_edit TEXT, user_id INTEGER)')
    temp2 = c.execute(f'SELECT edit_id FROM {story_name}').fetchall()
    edit_id = len(temp2) + 1
    #print(c.execute(f'SELECT * FROM {story_name}').fetchall())
    #c.execute(f'INSERT INTO "{story_name}" VALUES ({edit_id}, "{newest_edit}", {user_id})')
    c.execute(f'INSERT INTO "{story_name}" VALUES (?,?,?)', (edit_id, newest_edit, user_id))
    username = db_users.get_username_from_id(user_id)
    db_users.add_into_user_db(username, story_id, edit_id)
    #print(c.execute('SELECT * FROM main').fetchall())
    db.commit() #save changes
    return 1
    #db.close()  #close database
def get_random_article():
    temp1 = c.execute("SELECT story_id FROM main").fetchall()
    num = random.randint(0, len(temp1) - 1)
    return temp1[num][0]

def addlike(story_name):
    current_like = _select_from_main("like", story_name, 'story_name')
    current_like = current_like + 1
    c.execute(f'UPDATE main SET like = {current_like} WHERE story_name = "{story_name}"')
    db.commit()

add_entry('Story1', 'Avinda\'s board did not work.', 1, False)
    # add_entry('Story3', 'Avinda\'s board did not work part 2.', 1, False)
    # print(c.execute("SELECT * FROM main").fetchall())
    # addlike('Hello_World')
