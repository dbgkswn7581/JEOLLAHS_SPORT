from pydoc import describe
import discord
from discord import Intents
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

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
    

bot.run('token')