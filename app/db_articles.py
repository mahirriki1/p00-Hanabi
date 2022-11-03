import sqlite3
class db_articles:
    db = sqlite3.connect("articles.db")
    c = db.cursor()
    def select_from_main(data_want, data_give, datatype_give):
        db = sqlite3.connect("articles.db")
        c = db.cursor()
        print((c.execute(f'SELECT {data_want} FROM main WHERE {datatype_give}="{data_give}"')).fetchall())

    def select(story_name, data):
        print((c.execute(f"{data} IN {story_name}")))

    def add_entry(story_name, newest_edit, user_id):
        c.execute(f"CREATE TABLE main(story_id INTEGER, story_name TEXT, full_story TEXT, most_recent TEXT, user_id INTEGER) if not exists")
        temp1 = c.execute("SELECT story_id FROM main")
        story_id= len(temp1) + 1
        story_id = c.execute(f'SELECT story_id WHERE story_name="{story_name}" if {story_name} IN story_name')
        full_story_pre = c.execute(f'SELECT full_story WHERE story_name="{story_name}"')
        c.execute(f"INSERT into main({story_id}, story_name, )")
        c.execute(f"CREATE TABLE {story_name}(edit_id INTEGER, story_addition TEXT, user_id INTEGER) if not exists")
        #c.execute(f"INSERT into {story_name}()
    c.execute("CREATE TABLE if not exists main(story_id INTEGER, story_name TEXT, full_story TEXT, most_recent TEXT, user_id INTEGER)")
    c.execute("INSERT into main VALUES('1', 'story1', 'ogaboogahooda', 'bpp', '17')")
    select_from_main('story_id', 17, 'user_id')

