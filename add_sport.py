import discord
import sqlite3

admin_id_list = [323269908886454272, 277367977915973634]

def add_sport(ctx, sort, team1, team2, time):
    if ctx.author.id not in admin_id_list:
        return "관리자가 아닙니다."
    
    else:
        conn = sqlite3.connect('sport.db', isolation_level=None)
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM sport')
        cnt = len(cur.fetchall())
        
        num = cnt + 1
        
        cur.execute('INSERT INTO sport(num, sort, time, team1, team2, score_team1, score_team2, current, result) VALUES(?,?,?,?,?,?,?,?,?)',(num, sort, time, team1, team2, 0, 0, 1, 0))
        
        cur.close()
        conn.close()
        
        embed = discord.Embed(
            title = "경기 추가 완료",
            description = "%d번째 경기 추가" %num,
            color = discord.Color.purple()
        )
        embed.add_field(
            name="종목",
            value=sort,
            inline="True"
        )
        embed.add_field(
            name="시간",
            value=time,
            inline="True"
        )
        embed.add_field(
            name="팀1",
            value=team1,
            inline="True"
        )
        embed.add_field(
            name="팀2",
            value=team2,
            inline="True"
        )
        
        return embed
    
def del_sport(ctx, sport_index):
    if ctx.author.id not in admin_id_list:
        return "관리자가 아닙니다."
    
    else:
        conn = sqlite3.connect('sport.db', isolation_level=None)
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM sport WHERE num=%d' %sport_index)
        sport_data = cur.fetchone()
          
        if sport_data == None:
            return "존재하지 않는 경기입니다."
        else:
            cur.execute('DELETE FROM sport WHERE num=%d' %sport_index)
        
            cur.close()
            conn.close()
            
            embed = discord.Embed(
                title = "경기 삭제 완료",
                description = "%d번째 경기 삭제" %sport_index,
                color = discord.Color.dark_gold()
            )            
            return embed
        
def change_sport(ctx, sport_index):
    if ctx.author.id not in admin_id_list:
        return "관리자가 아닙니다."
    
    else:
        conn = sqlite3.connect('sport.db', isolation_level=None)
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM sport WHERE num=%d' %sport_index)
        sport_data = cur.fetchone()
          
        if sport_data == None:
            return "존재하지 않는 경기입니다."
        elif sport_data[7] != 1:
            return "이미 진행 중이거나 종료된 경기입니다."
        else:
            cur.execute('UPDATE sport SET current=%d WHERE num=%d' %(2, sport_index))
        
            cur.close()
            conn.close()
            
            embed = discord.Embed(
                title = "경기 변경 완료",
                description = "%d번째 경기 진행 중으로 변경" %sport_index,
                color = discord.Color.dark_grey()
            )            
            return embed
        
def end_sport(ctx, sport_index, score_team1, score_team2, result):
    if ctx.author.id not in admin_id_list:
        return "관리자가 아닙니다."
    
    else:
        conn = sqlite3.connect('sport.db', isolation_level=None)
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM sport WHERE num=%d' %sport_index)
        sport_data = cur.fetchone()
          
        if sport_data == None:
            return "존재하지 않는 경기입니다."
        elif sport_data[7] == 3:
            return "이미 종료된 경기입니다."
        else:
            cur.execute('UPDATE sport SET current=%d WHERE num=%d' %(3, sport_index))
            cur.execute('UPDATE sport SET score_team1=%d WHERE num=%d' %(score_team1, sport_index))
            cur.execute('UPDATE sport SET score_team2=%d WHERE num=%d' %(score_team2, sport_index))
            cur.execute('UPDATE sport SET result=%d WHERE num=%d' %(result, sport_index))
        
            cur.close()
            conn.close()
            
            embed = discord.Embed(
                title = "경기 변경 완료",
                description = "%d번째 경기 완료로 변경" %sport_index,
                color = discord.Color.dark_blue()
            )            
            return embed