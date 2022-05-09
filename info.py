import discord
import sqlite3
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def info(ctx):
    user_id = ctx.author.id
    conn = sqlite3.connect('user.db', isolation_level=None)
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM student_info WHERE id=%d' %user_id)
    exist = cur.fetchone()
    
    if exist != None:
        cur.close()
        conn.close()
        
        games = exist[4]
        
        embed = discord.Embed(
            title = '%d %s' %(exist[1], exist[2]),
            description = '보유 자금 : %s' %format(exist[3], ',') + "원",
            color = 0x81D3EB
        )
        
        for i in games:
            embed.add_field(
                name = i['sport'],
                value = '```diff\n[%s] vs [%s]```'%(i['team1'], i['team2']),
                inline = True
            )
            embed.add_field(
                name = "예측 > " + i['score'],
                value = "```diff\n'배율 : %d배'```"%(i['times']),
                inline = True
            )
            embed.add_field(
                name = '배팅액',
                value = '```diff\n#%s원```'%format(i['bet'], ','),
                inline = True
            )

    else:
        cur.close()
        conn.close()
        
        embed = discord.Embed(
            title = '시스템에 등록하지 않은 계정입니다.',
            description = "Jeolla HS Sports",
            color = discord.Color.red()
        )
        return embed
    