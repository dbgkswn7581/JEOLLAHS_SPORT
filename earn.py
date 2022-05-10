import discord
import sqlite3

def earn(ctx):
    user_id = ctx.author.id
    
    conn = sqlite3.connect('sport.db', isolation_level=None)
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM sport WHERE current=%d' %3)
    end_sport = cur.fetchall()
    end_sport_num_list = []
    
    for i in end_sport():
        end_sport_num_list.append(i[0])
    
    cur.close()
    conn.close()
    
    conn = sqlite3.connect('user.db', isolation_level=None)
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM student_info WHERE id=%d' %user_id)
    user_data = cur.fetchone()
    
    user_bet = user_data[3].split('//')[1:]
    earn_money_list = []
    
    for i in user_bet:
        tmp = i.split(',')
        if tmp[1] in end_sport_num_list:
            earn_money_list.append()
