from pydoc import describe
from zipapp import create_archive
import discord
from discord import Intents
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

bot = commands.Bot(command_prefix="!", intents=Intents.default())
slash = SlashCommand(bot, sync_commands=True)
channel_ids = [804340360519876629, 423837070906097664]

@slash.slash(   #가입
    name = '가입',
    description = "계정을 시스템에 신규 등록합니다.",
    options=[
        create_option(
            name='학번',
            description="본인의 학번을 적어주세요. ex) 2학년 3반 17번 -> 20317",
            option_type = 4,
            required = True
        ),
        create_option(
            name='이름',
            description="본인의 이름을 적어주세요.",
            option_type = 3,
            required = True
        )
    ],
    connector = {'학번' : 'student_number', '이름' : 'student_name'},
    guild_ids=channel_ids
)

async def reg(ctx: SlashCommand, student_number, student_name):
    from reg import reg
    embed = reg(ctx, student_number, student_name)
    await ctx.send(embed=embed)
    
@slash.slash(   #탈퇴
    name = '탈퇴',
    description = "시스템에서 계정을 제거합니다.",
    guild_ids=channel_ids
)

async def unreg(ctx: SlashCommand):
    from unreg import unreg
    embed = unreg(ctx)
    await ctx.send(embed=embed)
    
# @slash.slash(   #내 정보 -> 정보
#     name = '정보',
#     description = "본인 계정의 정보를 확인합니다.",
#     guild_ids=channel_ids
# )

# async def info(ctx: SlashCommand):
#     from info import info
#     embed = info(ctx)
#     await ctx.send(embed=embed)

@slash.slash(   #경기
    name = '경기',
    description = "예정/진행/완료된 경기에 대한 정보를 확인합니다.",
    options=[
        create_option(
            name='현황',
            description="예정/진행/종료 중 아무것도 입력하지 않으면, 기본값인 '진행'으로 지정됩니다.",
            option_type = 3,
            required = True,
            choices=[
                create_choice(
                    name="예정",
                    value="expect"
                ),
                create_choice(
                    name="진행",
                    value="progress"
                ),
                create_choice(
                    name="종료",
                    value="close"
                )
            ]
        ),
        create_option(
            name='페이지',
            description="보고 싶은 페이지를 입력하세요. 아무것도 입력하지 않으면 기본값인 1페이지를 보게 됩니다.",
            option_type= 4,
            required=True
        ),       
        
    ],
    connector={'현황':'choose_sport', '페이지':'input_page'},
    guild_ids=channel_ids
)

async def sport(ctx: SlashCommand, choose_sport: str = 'expect', input_page: int = 1):   
    from sport import sport
    embed = sport(ctx, choose_sport, input_page)
    
    if type(embed) == str: 
        await ctx.send(embed)
    else:
        await ctx.send(embed=embed)
        
@slash.slash(   #배팅
    name = '배팅',
    description = "예정된 경기이거나 진행 중인 경기에 배팅을 합니다.",
    options=[
        create_option(
            name='인덱스',
            description="어떤 인덱스의 경기에 배팅할 건지 입력합니다.",
            option_type = 4,
            required = True,
        ),
        create_option(
            name='배팅액',
            description="얼만큼 배팅할 건지 입력합니다.",
            option_type= 4,
            required=True
        ),
        create_option(
            name='예측1',
            description="팀1이 몇 점을 얻을 지 예측합니다. 비긴다에 배팅할 경우 999를 입력합니다.",
            option_type= 4,
            required=True
        ),
        create_option(
            name='예측2',
            description="팀2가 몇 점을 얻을 지 예측합니다. 비긴다에 배팅할 경우 999를 입력합니다.",
            option_type= 4,
            required=True
        )
        
    ],
    connector={'인덱스':'sport_num', '배팅액':'bet_money', '예측1':'input_score_team1', '예측2' : 'input_score_team2'},
    guild_ids=channel_ids
)

async def bet(ctx: SlashCommand, sport_num: int, bet_money: int, input_score_team1: int, input_score_team2: int):   
    from bet import bet
    embed = bet(ctx, sport_num, bet_money, input_score_team1, input_score_team2)
    
    if type(embed) == str: 
        await ctx.send(embed)
    else:
        await ctx.send(embed=embed)

@slash.slash(   #경기 추가 // 관리자
    name = '추가',
    description = "경기를 추가합니다.",
    options=[
        create_option(
            name='종목',
            description="축구:1,농구:2,탁구:3,배드민턴:4,계주:5 중 입력(숫자로!!)",
            option_type = 4,
            required = True,
        ),
        create_option(
            name='팀1',
            description="3학년 8반 -> 0308",
            option_type= 3,
            required=True
        ),
        create_option(
            name='팀2',
            description="1학년 10반 -> 0110",
            option_type= 3,
            required=True
        ),
        create_option(
            name='시간',
            description="2시 20분 -> 14:20 (24시 표기)",
            option_type= 3,
            required=True
        )
    ],
    connector={'종목':'sort', '팀1':'team1', '팀2':'team2', '시간':'time'},
    guild_ids=channel_ids
)

async def add_sport(ctx: SlashCommand, sort: int, team1: str, team2: str, time: str):
    from add_sport import add_sport
    embed = add_sport(ctx, sort, team1, team2, time)
    
    if type(embed) == str: 
        await ctx.send(embed)
    else:
        await ctx.send(embed=embed)

@slash.slash(   #경기 삭제 // 관리자
    name = '삭제',
    description = "경기를 삭제합니다.",
    options=[
        create_option(
            name='번호',
            description="경기의 인덱스 입력",
            option_type = 4,
            required = True,
        )
    ],
    connector={'번호':'sport_index'},
    guild_ids=channel_ids
)

async def del_sport(ctx: SlashCommand, sport_index: int):
    from add_sport import del_sport
    embed = del_sport(ctx, sport_index)
    
    if type(embed) == str: 
        await ctx.send(embed)
    else:
        await ctx.send(embed=embed)

@slash.slash(   #경기 중 상태로 변경 // 관리자
    name = '변경',
    description = "경기 중인 상태로 변경합니다.",
    options=[
        create_option(
            name='번호',
            description="경기의 인덱스 입력",
            option_type = 4,
            required = True,
        )
    ],
    connector={'번호':'sport_index'},
    guild_ids=channel_ids
)

async def change_sport(ctx: SlashCommand, sport_index: int):
    from add_sport import change_sport
    embed = change_sport(ctx, sport_index)
    
    if type(embed) == str: 
        await ctx.send(embed)
    else:
        await ctx.send(embed=embed)
        
@slash.slash(   #경기 완료 상태로 변경 // 관리자
    name = '종료',
    description = "경기 완료 상태로 변경합니다.",
    options=[
        create_option(
            name='번호',
            description="경기의 인덱스 입력",
            option_type = 4,
            required = True,
        ),
        create_option(
            name='팀1_점수',
            description="팀1의 획득 점수 입력",
            option_type = 4,
            required = True,
        ),
        create_option(
            name='팀2_점수',
            description="팀2의 획득 점수 입력",
            option_type = 4,
            required = True,
        ),
        create_option(
            name='우승팀',
            description="팀1이 우승: 1, 팀2가 우승: 2, 무승부: 3",
            option_type = 4,
            required = True,
        )
    ],
    connector={'번호':'sport_index', '팀1_점수':'score_team1', '팀2_점수':'score_team2','우승팀':'result'},
    guild_ids=channel_ids
)

async def end_sport(ctx: SlashCommand, sport_index: int, score_team1: int, score_team2: int, result: int):
    from add_sport import end_sport
    embed = end_sport(ctx, sport_index, score_team1, score_team2, result)
    
    if type(embed) == str: 
        await ctx.send(embed)
    else:
        await ctx.send(embed=embed)
        
@slash.slash(   
    name = '정산',
    description = "본인이 배팅한 경기 중 완료된 경기의 결과를 정산합니다.",
    guild_ids=channel_ids
)

async def earn(ctx: SlashCommand):
    from earn import earn
    embed = earn(ctx)
    
    if type(embed) == str: 
        await ctx.send(embed)
    else:
        await ctx.send(embed=embed)

bot.run('OTcwOTQ5MTQ5MzYzMTU0OTc0.YnDY3A.feRULbkblQ-GIMeJER76l4rKW9c')
