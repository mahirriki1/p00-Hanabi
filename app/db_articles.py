import sqlite3
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
def get_newest_edit(story_name):
    return _select_from_main('most_recent', story_name, 'story_name')
#def get_all_story(user_id):

def get_full_story(story_id):
    return _select_from_main('full_story', story_id, 'story_id')

def add_entry(story_name, newest_edit, user_id):
    story_exist = True
    pre_story = ""
    c.execute("CREATE TABLE if not exists main(story_id INTEGER PRIMARY KEY, story_name TEXT, full_story TEXT, most_recent TEXT, user_id INTEGER)")
    temp1 = c.execute("SELECT story_id FROM main").fetchall()
    story_id = (_select_from_main('story_id', story_name, 'story_name'))
    prev_add = (_select_from_main('most_recent', story_name, 'story_name'))
    if(story_id == 0):
          story_exist = False
          story_id = len(temp1) + 1
    if(story_exist):
        pre_story = get_full_story(story_name)
    new_full = pre_story + " " + newest_edit
    c.execute(f'INSERT OR REPLACE INTO main(story_id, story_name, full_story, most_recent, user_id) VALUES ({story_id}, "{story_name}", "{new_full}", "{newest_edit}", {user_id})')
    c.execute(f'CREATE TABLE if not exists "{story_name}"(edit_id INTEGER PRIMARY KEY, newest_edit TEXT, user_id INTEGER)')
    temp2 = c.execute(f'SELECT edit_id FROM {story_name}').fetchall()
    edit_id = len(temp2) + 1
    #print(c.execute(f'SELECT * FROM {story_name}').fetchall())
    c.execute(f'INSERT INTO "{story_name}" VALUES ({edit_id}, "{newest_edit}", {user_id})')
    #print(c.execute('SELECT * FROM main').fetchall())
    db.commit() #save changes
    db.close()  #close database
#add_entry('Hello_World', 'Welcome to the new worlda', 14)

