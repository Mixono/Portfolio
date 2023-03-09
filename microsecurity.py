import interactions
from interactions import *
from colorama import *
import time
import json
import datetime
import os

# Not Completed btw

micro = interactions.Client("MTA3ODg3ODcyOTQ1MjkyOTA1NQ.GMxEm_.9Zog-kt0qXADg9zxF8-PI_8mno_weqqkTgT9aA",
    presence=interactions.ClientPresence(
        status=interactions.StatusType.ONLINE,
        activities=[
            interactions.PresenceActivity(name="with Micro Community", type=interactions.PresenceActivityType.GAME)
        ]
    )
)

# Global Dev Only Embed
devonly = interactions.Embed(title=f':robot: Developer Only Command!', color=0x3371FF)
devonly.add_field(name=f'What Happened?', value='This Command is still in **BETA** or it is a developer only command!', inline=False),

@micro.event
async def on_start():
    print(Fore.CYAN + f'[Micro] ' + Fore.BLUE + 'Successfully logged in!')

# Commands

@micro.command(name='help', description='Displays all commands for Micro', default_member_permissions=interactions.Permissions.ADMINISTRATOR)
async def info(ctx):
    helpcmd = interactions.Embed(title=':memo: Help Commands', color=0x82FF33)
    helpcmd.add_field(name=':name_badge: | Admin Commands', value='```N/A```', inline=True)
    helpcmd.add_field(name=':shield: | Security Commands', value='```N/A```', inline=True)
    helpcmd.add_field(name=':man_detective: | Moderator Commands', value='```N/A```', inline=True)
    await ctx.send(embeds=helpcmd)

@micro.command(name='setup', description='Connect your server information to our Security Systems', default_member_permissions=interactions.Permissions.ADMINISTRATOR)
async def setup(ctx):
    def doesFileExists(filePathAndName):
        return os.path.exists(filePathAndName)

    if doesFileExists(f'{ctx.guild.id}.json'):
        setupfail = interactions.Embed(title=':x: Connection Error', color=0xFF2626)
        setupfail.add_field(name='What Happened?', value='It appears that your server is already setup. If you think this is a error feel free to submit a bug report with `/issue`', inline=False)
        setupfail.add_field(name='Extra:', value='Do `/help` for all commands!', inline=False)
        await ctx.send(embeds=setupfail)
    else:
        setupstart = interactions.Embed(title=':memo: Setup Starting...', color=0x82FF33)
        setupstart.add_field(name='Connecting to Database...', value='This may take more than a minute.', inline=False)
        await ctx.send(embeds=setupstart)
        with open(f'{ctx.guild.id}.json', 'w'):
            setupdb = {
                "server-id": f"{ctx.guild.id}",
                "punishment-manager": "Off",
                "punishment-manager-channel": "None",
                "date": f'{datetime.date.today()}',
            }
            setupdump = json.dumps(setupdb)
            file = open(f'{ctx.guild.id}.json', 'w')
            file.write(setupdump)
            file.close
            time.sleep(3) 
            setupend = interactions.Embed(title=':memo: Setup Success!', color=0x82FF33)
            setupend.add_field(name='What Happened?', value='*We have connected your Server Information to our Security Systems!*', inline=False)
            setupend.add_field(name='Extra:', value='Do `/help` for all commands!', inline=False)
            await ctx.send(embeds=setupend)

@micro.command(name='settings', description='Displays all your Server Security Settings', default_member_permissions=interactions.Permissions.ADMINISTRATOR)
async def settings(ctx):
    with open(f'{ctx.guild.id}.json', 'r') as check:
        checker = json.load(check)
        settings = interactions.Embed(title=f':memo: Security Settings', color=0x26BBFF)
        settings.add_field(name='Overall Status:', value=checker["micro-mode"], inline=False)
        await ctx.send(embeds=settings)

@micro.command(description='Select a user to ban', default_member_permissions=interactions.Permissions.ADMINISTRATOR)
@interactions.option("Select the user you will like to ban", required=True)
@interactions.option("Enter a reason for this ban", required=True)
async def ban(ctx: interactions.CommandContext, user: interactions.Member, reason: str):
    bancmd = interactions.Embed(title=f':name_badge: Ban Information', color=0xFF3333)
    bancmd.add_field(name=f'Name:', value=f'{user.name}', inline=False),
    bancmd.add_field(name='ID:', value=f'{user.id}', inline=False),
    bancmd.add_field(name='Date Joined: ', value=f'{user.joined_at}', inline=False),
    bancmd.add_field(name='Reason Banned:', value=f'{reason}', inline=False)
    banbutton = Button(style=4, label=f"❓ Learn More", custom_id="banbutton")
    await ctx.guild.ban(member_id=user.id, reason=reason)
    await ctx.send(embeds=bancmd, components=banbutton, ephemeral=True)
    with open(f'{ctx.guild.id}.json', 'r') as servercheck:
        punishcheck = json.load(servercheck)
        pmanagercheck = punishcheck["punishment-manager"]
        channel1 = punishcheck["punishment-manager-channel"]
        channel = await interactions.get(micro, interactions.Channel, object_id=channel1)
        if pmanagercheck == "On":
            bancmdinfo = interactions.Embed(title=f':bell: Punishment Manager | Ban Information', color=0xFF3333)
            bancmdinfo.add_field(name=f'Moderator:', value=f'{ctx.author.mention}', inline=False),
            bancmdinfo.add_field(name=f'User Banned:', value=f'{user.name}', inline=False),
            bancmdinfo.add_field(name='User ID:', value=f'{user.id}', inline=False),
            bancmdinfo.add_field(name='Date User Joined: ', value=f'{user.joined_at}', inline=False),
            bancmdinfo.add_field(name='Reason Banned:', value=f'{reason}', inline=False)
            await channel.send(embeds=bancmdinfo)

@micro.component("banbutton")
async def infoban(ctx):
    await ctx.author.send(embeds=devonly)

@micro.component("kickbutton")
async def infokick(ctx):
    await ctx.author.send(embeds=devonly)

@micro.component("warnbutton")
async def infowarn(ctx):
    await ctx.author.send(embeds=devonly)


@micro.command(description='Select a user to kick', default_member_permissions=interactions.Permissions.ADMINISTRATOR)
@interactions.option("Select the user you will like to kick", required=True)
@interactions.option("Enter a reason for this kick", required=True)
async def kick(ctx: interactions.CommandContext, user: interactions.Member, reason: str):
    kickcmd = interactions.Embed(title=f':zap: Kick Information', color=0xFF3333)
    kickcmd.add_field(name=f'Name:', value=f'{user.name}', inline=False),
    kickcmd.add_field(name='ID:', value=f'{user.id}', inline=False),
    kickcmd.add_field(name='Date Joined: ', value=f'{user.joined_at}', inline=False),
    kickcmd.add_field(name='Reason Kicked:', value=f'{reason}', inline=False)
    kickbutton = Button(style=4, label=f"❓ Learn More", custom_id="kickbutton")
    await ctx.guild.kick(member_id=user.id, reason=reason)
    await ctx.send(embeds=kickcmd, components=kickbutton, ephemeral=True)
    with open(f'{ctx.guild.id}.json', 'r') as servercheck:
        punishcheck = json.load(servercheck)
        pmanagercheck = punishcheck["punishment-manager"]
        channel1 = punishcheck["punishment-manager-channel"]
        channel = await interactions.get(micro, interactions.Channel, object_id=channel1)
        if pmanagercheck == "On":
            kickcmdinfo = interactions.Embed(title=f':bell: Punishment Manager | Kick Information', color=0xFF3333)
            kickcmdinfo.add_field(name=f'Moderator:', value=f'{ctx.author.mention}', inline=False),
            kickcmdinfo.add_field(name=f'User Kicked:', value=f'{user.name}', inline=False),
            kickcmdinfo.add_field(name='User ID:', value=f'{user.id}', inline=False),
            kickcmdinfo.add_field(name='Date User Joined: ', value=f'{user.joined_at}', inline=False),
            kickcmdinfo.add_field(name='Reason Kicked:', value=f'{reason}', inline=False)
            await channel.send(embeds=kickcmdinfo)

@micro.command(description='Select a user to warn', default_member_permissions=interactions.Permissions.ADMINISTRATOR)
@interactions.option("Select the user you will like to warn", required=True)
@interactions.option("Enter a reason for this warn", required=True)
async def warn(ctx: interactions.CommandContext, user: interactions.Member, reason: str):
    warnmsg = interactions.Embed(title=f':dart: Warn Information', color=0xFF3333)
    warnmsg.add_field(name=f'Name:', value=f'{user.name}', inline=False),
    warnmsg.add_field(name='ID:', value=f'{user.id}', inline=False),
    warnmsg.add_field(name='Warned For:', value=f'{reason}', inline=False)
    warnbutton = Button(style=4, label=f"❓ Learn More", custom_id="warnbutton")
    warncmd = interactions.Embed(title=f':dart: Warn Information', color=0xFF3333)
    warncmd.add_field(name=f'Name:', value=f'{user.name}', inline=False),
    warncmd.add_field(name='ID:', value=f'{user.id}', inline=False),
    warncmd.add_field(name='Date Joined: ', value=f'{user.joined_at}', inline=False),
    warncmd.add_field(name='Reason Warned:', value=f'{reason}', inline=False)
    await user.send(embeds=warnmsg)
    await ctx.send(embeds=warncmd, components=warnbutton, ephemeral=True)
    with open(f'{ctx.guild.id}.json', 'r') as servercheck:
        punishcheck = json.load(servercheck)
        pmanagercheck = punishcheck["punishment-manager"]
        channel1 = punishcheck["punishment-manager-channel"]
        channel = await interactions.get(micro, interactions.Channel, object_id=channel1)
        if pmanagercheck == "On":
            warncmdinfo = interactions.Embed(title=f':bell: Punishment Manager | Warn Information', color=0xFF3333)
            warncmdinfo.add_field(name=f'Moderator:', value=f'{ctx.author.mention}', inline=False),
            warncmdinfo.add_field(name=f'User Warned:', value=f'{user.name}', inline=False),
            warncmdinfo.add_field(name='User ID:', value=f'{user.id}', inline=False),
            warncmdinfo.add_field(name='Date User Joined: ', value=f'{user.joined_at}', inline=False),
            warncmdinfo.add_field(name='Reason Warned:', value=f'{reason}', inline=False)
            await channel.send(embeds=warncmdinfo)

@micro.command(name='issue', description='Report a Issue with Micro to our Developement Team')
@interactions.option("Tell us the issue you are having", required=True)
async def issue(ctx, issue: str):
    with open(f'{ctx.author.id} Issue.json', 'w'):
            issuereport = {
                "user-id": f"{ctx.author.id}",
                "issue": f"{issue}",
                "date": f'{datetime.date.today()}',
            }
            issuedump = json.dumps(issuereport)
            file = open(f'{ctx.author.id} Issue.json', 'w')
            file.write(issuedump)
            file.close
            issuecmd = interactions.Embed(title=f':ballot_box: Issue Submitted', color=0xFFA926)
            issuecmd.add_field(name='Author:', value=f'{ctx.author.mention}', inline=False),
            issuecmd.add_field(name='Issue:', value=f'`{issue}`', inline=False)
            issuecmd.add_field(name='Date:', value=f'{datetime.date.today()}', inline=False),
            await ctx.author.send(embeds=issuecmd)


@micro.command(name='ping', description='Replies with pong. Or does it?', default_member_permissions=interactions.Permissions.ADMINISTRATOR)
async def ping(ctx):
     with open('devlist.json', 'r') as devs:
        devlist = json.load(devs)
        developers = devlist["devs"]
        if ctx.author.id == developers:
            ping = interactions.Embed(title=f':robot: Bot Latency', color=0xFFA926)
            ping.add_field(name='Current Status', value=f'Bot Latency is as fast as `{round(micro.latency * 1000)}` milliseconds', inline=False)
            await ctx.send(embeds=ping)
        else:
            await ctx.send(embeds=devonly)

    

micro.start()
