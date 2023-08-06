import discord
from discord.ext import commands
from evediscordbot import dbCalls as db

import os

var_key = os.environ['var_bot']
bot2_prefix= "~"
bot_prefix= "!"
bot = commands.Bot(command_prefix=bot_prefix)



@bot.event
async def on_ready():
    print("Eve is online ;)")
    print("Name: {}".format(bot.user.name))
    print("ID: {}".format(bot.user.id))

@bot.command()
async def addall(ctx,role: discord.Role=None):
    '''Assigns all users in discord with specified role'''

    try:

        if (role.permissions.administrator == True):
            await ctx.send("Nice try buddy, no admin for everyone.")
        elif(ctx.author.top_role.permissions.administrator == False):
            await ctx.send(" u aint no admin bish")
        else:
            for member in bot.get_all_members():
                if role not in member.roles:
                    await member.add_roles(role,reason="For vote thing")
            await ctx.send(str(role) +" role Added to all members")
    except:
        await ctx.send("ERROR: That is not a valid role on this server")
 # !removeall @test 569766779308736532

@bot.command()
async def removeall(ctx,role: discord.Role=None):
    '''Removes specified role from all users in the discord'''
    try:

        if (role.permissions.administrator == True):
            await ctx.send("No.")
        elif (ctx.author.top_role.permissions.administrator == False):
            await ctx.send(" u aint no admin bish")
        else:
            for member in bot.get_all_members():

                if role in member.roles:
                    tempuser = member

                    await tempuser.remove_roles(role)
            await ctx.send(str(role) + " role removed from all members")
    except:
        await ctx.send("ERROR: That is not a valid role on this server")

@bot.command()
async def getroles(ctx,x = None):
    '''If passed a user this command lists all roles for that user, otherwise lists all roles in server'''
    try:
        await ctx.send(str(bot.guilds))

    except:
        await ctx.send("you dun goofed matt")





@bot.command()
async def addstrike(ctx,userID : discord.User):
    '''Adds strike for specified user'''

    if (ctx.author.top_role.permissions.kick_members == True or ctx.author.top_role.permissions.administrator):
        db.enterStrike(userID=str(userID.id), username=str((userID)))
        await ctx.send("strike added for " + str(userID) + ", this user now has " + str(db.getStrikes(str(userID.id))) + " strikes")
    else:
        await ctx.send("You need mod permissions to use this command")






@bot.command()
async def clearstrikes(ctx,userID : discord.User):
        '''Clears ALL strikes for specified user'''
        if (ctx.author.top_role.permissions.kick_members == True or ctx.author.top_role.permissions.administrator):
            db.clearStrikes(str(userID.id))
            await ctx.send("All strikes cleared for " + str(userID))

        else:
            await ctx.send("You need mod permissions to use this command")


@bot.command()
async def getstrikes(ctx,userID : discord.User):
    '''Lists all strikes for specified user ID'''
    db.getStrikes(str(userID.id))
    await ctx.send(str(userID) +" has " + str(db.getStrikes(str(userID.id))) + " strikes")




@bot.command()
async def strikelist(ctx):
    '''Lists strike count for all users with strikes'''
    await ctx.send("```"+db.getallStrikes()+"```")

'''@bot.command()
async def auditlog(ctx):

    async for entry in bot.get_guild(222402041618628608).audit_logs():
        await ctx.send('{0.user} banned {0.target}'.format(entry))
'''







'''@bot.command()
async def test(ctx):
    await ctx.send(bot.get_guild(222402041618628608).get_member(143220159312691202).top_role.permissions.kick)'''

bot.run(var_key)
