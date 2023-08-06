from .db_connection import DbConnection
from datetime import datetime

class Dsm:
    """ 
    The DSM package can be used to manage daily tasks and view them.
    """

    def __init__(self):
        self.connection_obj = DbConnection() # Create a connection object
        self.connection_obj.create_table_if_not_exist() # Create table if it does not already exists

    def start(self):
        """ Function to start recording tasks """

        while True:
            activity_detail = input('Enter your activity : ')
            break_points = ['exit','q','e','']
            if activity_detail.lower() in break_points:
                break
            self.connection_obj.store_task(activity_detail)

    def show(self, *args):
        """ Function to show list of tasks on a particular date """

        dates = []
        if len(args) > 0:
            try:
                dates = [datetime.strptime(date, '%d-%m-%Y') for date in args]
            except Exception as e:
                return str(e)
        else:
            dates.append(datetime.now().date())
        return self.connection_obj.fetch_tasks(dates)

    def __del__(self):
        del self.connection_obj

def start():
    dsmobj = Dsm()
    dsmobj.start()
    del dsmobj

def show(*args):
    dsmobj = Dsm()
    records = dsmobj.show(*args)
    if type(records) is list:
        for rec in records:
            date_format = datetime.strptime(rec[2],"%Y-%m-%d %H:%M:%S.%f").strftime('%A, %d. %B %Y %I:%M%p')
            task_string = str(date_format)+' : '+str(rec[1])
            print(task_string)
    else:
        print(records)
    del dsmobj