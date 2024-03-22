from valorantMatch import valorantMatch
from discordService import discordService
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    bot.loop.create_task(loopMatch())

async def loopMatch():
    await bot.wait_until_ready()
    channel = bot.get_channel(859865425989599276) 
    match_instance = valorantMatch()
    discordServiceInstance = discordService()

    while not bot.is_closed():
        if match_instance.isLastMatchNew() is False:            
            match = match_instance.getMatchInfo()
            tab = discordServiceInstance.formatDescription(match)

            embed = discord.Embed(title="RELATÓRIO DA PARTIDA - VALORANT",
                      description=f"{tab}",
                      colour=0x00f510)

            embed.add_field(name="KDR", value=discordServiceInstance.getRatios(match, "kdRatio"), inline=True)
                                               
            embed.add_field(name="TAXA DE HS %", value=discordServiceInstance.getRatios(match, "hs"), inline=True)
                                           
            embed.add_field(name="CLUTCHES", value=discordServiceInstance.getRatios(match, "clutches"),  inline=True)
                                                     
            embed.add_field(name="ADR", value=discordServiceInstance.getRatios(match, "adr"), inline=True)
                                        
            embed.add_field(name="Score", value=discordServiceInstance.getRatios(match, "score"), inline=True)             
                           
            embed.add_field(name="Kills", value=discordServiceInstance.getRatios(match, "kills"), inline=True) 

            embed.set_image(url=discordServiceInstance.getMapImage(match))

            await channel.send(embed=embed)
            
        await asyncio.sleep(60)

bot.run("MTIyMDQzNzA5MTE4NDQxMDY0NA.G41sne.r_2t1Cb0sxPNLtREUXIbB4d8wbZvYEy_FkmWVc")

