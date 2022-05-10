import discord
import sqlite3

def reg(ctx, num, name):
    user_id = ctx.author.id
    conn = sqlite3.connect('user.db', isolation_level=None)
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM student_info WHERE id=%d' %user_id)
    exist = cur.fetchone()
    
    cur.execute('SELECT * FROM student_info WHERE number=%d' %num)
    exist_num = cur.fetchone()
    
    if exist == None and exist_num == None:
        cur.execute('INSERT INTO student_info(id, number, name, money, bet) \
            VALUES(?,?,?,?,?)', \
            (user_id, num, name, 100000, '//0'))
        conn.commit()
        
        cur.close()
        conn.close()
        
        embed = discord.Embed(
            title = '계정이 생성되었습니다.',
            description = "Jeolla HS Sports",
            color = discord.Color.green()
        )
        embed.add_field(name='학번', value = num, inline=True)
        embed.add_field(name='이름', value = name, inline=True)
        embed.add_field(name='초기 자금', value = '100,000원', inline=True)
        return embed
    elif exist != None:
        cur.close()
        conn.close()
        
        embed = discord.Embed(
            title = '이미 등록된 계정입니다.',
            description = "Jeolla HS Sports",
            color = discord.Color.red()
        )
        embed.add_field(name='학번', value = exist[1], inline=True)
        embed.add_field(name='이름', value = exist[2], inline=True)
        embed.add_field(name='자금', value = '%s원' %format(exist[3], ','), inline=True)
        return embed
    elif exist_num != None:
        cur.close()
        conn.close()
        
        embed = discord.Embed(
            title = '이미 등록된 학번입니다.',
            description = "Jeolla HS Sports",
            color = discord.Color.red()
        )
        return embed
