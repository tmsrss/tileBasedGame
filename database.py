import mysql.connector
import datetime
import tkinter  as tk
from tkinter import *
from tkintertable import TableCanvas, TableModel


def Convert(list):
    f={}
    c=0
    for z in list:
        v=('username', 'kills', 'UTC date & time')
        d=dict(zip(v, z))
        now = d['UTC date & time']
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        d['UTC date & time'] = date_time
        f[c]=d
        c+=1
    return f

def mergeSort(list, ascending=True):
    if len(list) > 1:
        mid = len(list) // 2
        left = list[:mid]
        right = list[mid:]
        mergeSort(left)
        mergeSort(right)
        i = 0
        j = 0
        k = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                list[k] = left[i]
                i += 1
            else:
                list[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            list[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            list[k] = right[j]
            j += 1
            k += 1
    if ascending == True:
        return list
    else:
        list.reverse()
        return list

def mergeSortDict(dict, ascending=True):
    listed = list(dict.values())
    listed = mergeSort(listed, ascending)
    orderedDict = {}
    for value in listed:
        for key in dict:
            if dict[key] == value:
                orderedDict[key] = value
    return orderedDict

def update_statistics(LOGGEDIN_PLAYERID, game):
    if LOGGEDIN_PLAYERID is not None or LOGGEDIN_PLAYERID != '':
        db = mysql.connector.connect(host='localhost', user='root', passwd='root', database='tiled_game')
        cursor = db.cursor()
        try:
            now = datetime.datetime.utcnow()
            sql = 'INSERT INTO data (playerID, kills, date) VALUES (%s, %s, %s)'
            val = (int(LOGGEDIN_PLAYERID), int(game.player.get_kills()), now)
            cursor.execute(sql, val)
            db.commit()
        except:
            print('ERROR Updating last game statistics')
            print('Last game progress has been lost.')


class display_database:
    def __init__(self):
        self.my_w = tk.Tk()
        self.my_w.geometry("600x300")
        self.my_w.title('Database Connector')
        self.db = mysql.connector.connect(host='localhost', user='root', passwd='root', database='tiled_game')
        self.cursor = self.db.cursor()

    def display_users(self):
        self.cursor.execute("SELECT COUNT(*) FROM tiled_game.player")
        res = self.cursor.fetchone()
        y = int((169/8) * (res[0]))
        self.my_w.geometry("153x%s" %y)
        self.cursor.execute('SELECT playerID, username FROM player LIMIT 0,10')
        i = 0
        for player in self.cursor:
            for j in range(len(player)):
                e = Label(self.my_w, width=10, text=player[j], borderwidth=2,relief='ridge', anchor="center")
                e.grid(row=i, column=j)
            i = i + 1
        # HEADINGS
        e = Label(self.my_w, width=10, text='playerID', borderwidth=2, relief='ridge', anchor='center', bg='yellow')
        e.grid(row=0, column=0)
        e = Label(self.my_w, width=10, text='Username', borderwidth=2, relief='ridge', anchor='center', bg='yellow')
        e.grid(row=0, column=1)
        # --------
        self.my_w.mainloop()

    def display_personal_statistics(self, LOGGEDIN_PLAYERID):
        self.cursor.execute('SELECT player.username, data.kills, data.date FROM data INNER JOIN player ON data.playerID = player.playerID WHERE player.playerID=%s ORDER BY date DESC', (LOGGEDIN_PLAYERID,))
        result = self.cursor.fetchall()
        data = Convert(result)
        tframe = Frame(self.my_w)
        tframe.pack()
        model = TableModel()
        table = TableCanvas(tframe, model=model, data=data, editable=False, width=800, height=300)
        table.show()
        self.my_w.mainloop()

    def SQL_ALTERNATIVE_display_leaderboard(self):
        '''
        display top 10 kills, by using sql limit
        then sort the list by using mergesort, with highest kill on top. Could have also used sql ORDER BY
        '''
        self.cursor.execute('SELECT player.username, MAX(data.kills) AS kills, data.date FROM data INNER JOIN player ON data.playerID = player.playerID GROUP BY username ORDER BY data.kills DESC limit 0, 10 ')
        result = self.cursor.fetchall()
        data = Convert(result)
        tframe = Frame(self.my_w)
        tframe.pack()
        model = TableModel()
        table = TableCanvas(tframe, model=model, data=data, editable=False, width=800, height=300)
        table.show()
        self.my_w.mainloop()

    def display_leaderboard(self):
        self.cursor.execute(
            'SELECT player.username, MAX(data.kills) AS kills, data.date FROM data INNER JOIN player ON data.playerID = player.playerID GROUP BY username limit 0, 10 ')
        result = self.cursor.fetchall()
        data = Convert(result)

        kills_dict = dict()
        for key in data:
            data_value=list(data[key].values())
            kills_dict[key] = data_value[1]

        kills_dict = mergeSortDict(kills_dict, ascending=False)

        final_dict = dict()

        for key in kills_dict:
            final_dict[key] = data[key]

        tframe = Frame(self.my_w)
        tframe.pack()
        model = TableModel()
        table = TableCanvas(tframe, model=model, data=final_dict, editable=False, width=800, height=300)
        table.show()
        self.my_w.mainloop()


if __name__ == '__main__':
    a = display_database()
    a.display_leaderboard()
