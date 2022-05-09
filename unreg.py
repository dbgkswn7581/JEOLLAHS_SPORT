import discord
import sqlite3

def unreg(ctx):
    user_id = ctx.author.id
    conn = sqlite3.connect('user.db', isolation_level=None)
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM student_info WHERE id=%d' %user_id)
    exist = cur.fetchone()
    
    if exist != None:
        cur.execute('DELETE FROM student_info WHERE id=%d' %user_id)
        conn.commit()
        
        cur.close()
        conn.close()
        
        embed = discord.Embed(
            title = '계정이 삭제되었습니다.',
            description = "Jeolla HS Sports",
            color = discord.Color.green()
        )
        embed.add_field(name='학번', value = exist[1], inline=True)
        embed.add_field(name='이름', value = exist[2], inline=True)
        embed.add_field(name='초기 자금', value = '%s원' %format(exist[3], ','), inline=True)
        return embed
    else:
        cur.close()
        conn.close()
        
        embed = discord.Embed(
            title = '시스템에 등록하지 않은 계정입니다.',
            description = "Jeolla HS Sports",
            color = discord.Color.red()
        )
        return embed
    