from pydoc import describe
import discord
import sqlite3

def bet(ctx, sport_num, bet_money, input_score_team1, input_score_team2):
    user_id = ctx.author.id
    conn = sqlite3.connect('sport.db', isolation_level=None)
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM sport WHERE num=%d' %sport_num)
    sport_data = cur.fetchone()
    
    cur.close()
    conn.close()
    
    conn = sqlite3.connect('user.db', isolation_level=None)
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM student_info WHERE id=%d' %user_id)
    user_data = cur.fetchone()
    
    if bet_money > user_data[3]:
        cur.close()
        conn.close()
        
        return "보유하신 돈보다 큰 금액을 배팅하셨습니다."
    elif sport_data[7] == 3:
        cur.close()
        conn.close()
        
        return "종료된 게임에 배팅할 수 없습니다."
    
    else:
        sportsort_list = [0, '축구', '농구', '탁구', '배드민턴', '계주']
                
        update_user_data = user_data[4]
        update_user_data = update_user_data + '//%d,%d,%d,%d'%(sport_num, bet_money, input_score_team1, input_score_team2)
        
        print(update_user_data, type(update_user_data))
        
        cur.execute('UPDATE student_info SET bet=? WHERE id=?', (update_user_data, user_id))
        cur.execute('UPDATE student_info SET money=? WHERE id=?', (user_data[3]-bet_money, user_id))

        cur.close()
        conn.close()
        
        embed = discord.Embed(
            title = "배팅이 완료되었습니다.",
            description = "역배에 성공 시 `2배`,\n스코어 정확히 맞출 시 `3배`,\n역배 및 스코어 정확히 맞출 시 `6배`",
            color=discord.Color.blue()
        )
        embed.add_field(
            name='종목',
            value=sportsort_list[int(sport_data[1])]
        )
        embed.add_field(
            name='팀1',
            value=sport_data[3]
        )
        embed.add_field(
            name='팀2',
            value=sport_data[4]
        )
        embed.add_field(
            name='예측',
            value=str(input_score_team1) +"(팀1)"+ " : " + str(input_score_team2) +"(팀2)"
        )
        embed.add_field(
            name='배팅액',
            value=bet_money
        )
        embed.add_field(
            name='남은 금액',
            value=user_data[3]-bet_money
        )
        
        return embed
        