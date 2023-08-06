import sqlite3
from datetime import datetime

class DbConnection:

    def __init__(self):
        try:
            self.connection = sqlite3.connect('dsm_records.db')
            self.cursorobj = self.connection.cursor()
        except Exception as e:
            return str(e)
    
    def create_table_if_not_exist(self):
        self.cursorobj.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task text, created_at text)")
        self.connection.commit()

    def store_task(self, task):
        try:
            now_datetime = datetime.now()
            self.cursorobj.execute("INSERT INTO tasks(task, created_at) VALUES('"+str(task)+"', '"+str(now_datetime)+"')")
            self.connection.commit()
        except Exception as e:
            return str(e)

    def fetch_tasks(self, dates):
        query_string = "SELECT * FROM tasks WHERE created_at BETWEEN DATE('"+str(dates[0])+"')"
        if len(dates) > 1:
            query_string+=" AND DATE('"+str(dates[1])+"')"
        else:
            query_string+=" AND DATE('"+str(dates[0])+"', '+1 day')"

        self.cursorobj.execute(query_string)
        rows = self.cursorobj.fetchall()
        return rows

    def __del__(self):
        self.connection.close()