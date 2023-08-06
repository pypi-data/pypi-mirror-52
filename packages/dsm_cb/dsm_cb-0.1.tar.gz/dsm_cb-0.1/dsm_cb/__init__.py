"""
DSM is a custom package to record daily tasks. It can be helpful in maintaining a log of tasks you did in the whole day.
The DSM package comes with two basic methods :

Use dsm.start() function to enter tasks. This function will store the task description with a timestamp.
Use dsm.show() function to get all the task of current day. The accepted date format is 'dd-mm-yyyy'
You can also pass a date string to get list of tasks on that particular date 
Or you can pass two dates to get list of tasks between those two dates.

Sample usage:

    import dsm
    dsm.show()

    OR

    import dsm
    dsm.show('19-09-2019')

    OR

    import dsm
    dsm.show('19-09-2019', '21-09-2019')

"""


from .start import *
