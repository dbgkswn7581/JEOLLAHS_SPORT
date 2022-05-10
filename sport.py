import discord
import sqlite3


# sport.db -> num, sort, time, team1, team2, score_team1, score_team2, current, result
#        ex->  1,  1 , 14:00,  0308,   0305,           2,           1,       3,     1
#num : index // sort : soccer - 1, basketball - 2, tabletennis - 3, bedminton - 4, race - 5 // time : 24시 표기 // team1/team2 : 0206 - 2학년 6반
#score_team1/score_team2 : 예정된 경기 or 진행 중인 경기 - 0vs0, 완료된 경기 - real score
#current : expect - 1, progress - 2, close - 3 // result : team1 win - 1, team2 win - 2, draw - 3

def sport(ctx, choose_sport, input_page):
    current_dic = {'expect' : 1, 'progress' : 2, 'close' : 3}
    current_name_dic = {'expect' : '예정된', 'progress' : '진행 중인', 'close' : '종료된'}
    sportsort_list = [0, '축구', '농구', '탁구', '배드민턴', '계주']
    
    conn = sqlite3.connect('sport.db', isolation_level=None)
    cur = conn.cursor()
    cur.execute('SELECT * FROM sport WHERE current=%d' %current_dic[choose_sport])
    
    sport_list = cur.fetchall()
    sport_list.reverse()
    
    cur.close()
    conn.close()
    
    pages = len(sport_list) / 10 + 1
    
    if input_page > pages:
        return "입력하신 페이지가 전체 페이지보다 큰 수입니다.\n다시 입력해주십시오."
    
    else:        
        embed = discord.Embed(
            title = "현재 " + current_name_dic[choose_sport] + " 경기들의 목록입니다.",
            description = "페이지 %d/%d"%(input_page, pages),
            color = 0xC295D7)
        
        for i in sport_list[10*(input_page-1):(10*input_page)-1]:
            embed.add_field(
                name=sportsort_list[int(i[1])],
                value=str(i[3]) + " vs " + str(i[4]),
                inline=True)
            
            embed.add_field(
                name = "Score " + str(i[5]) + ":" + str(i[6]),
                value = i[2],
                inline=True)
            
            result_list = [0, str(i[3]) + " win", str(i[4]) + " win", "draw"]
            
            embed.add_field(
                name = "INDEX %d" %i[0],
                value = result_list[int(i[8])],
                inline=True)
        
        return embed
        